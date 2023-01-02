from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ContentType, CallbackQuery

import models
from callback_data import SupportTicketDetailCallbackData
from filters import MessageLengthFilter
from services.api import SupportAPIClient, ShopInfoAPIClient
from shortcuts import answer_views, edit_message_by_view
from states import NewSupportRequestStates
from views import (
    SupportMenuView,
    SupportTicketCreatedView,
    RequireTicketIssueView,
    SupportTicketsListView,
    SupportRequestDetailView,
    AcceptSupportRulesView,
    RequireTicketSubjectView,
)

__all__ = ('register_handlers',)


# Validators
async def on_support_ticket_issue_length_too_long(message: Message) -> None:
    await message.answer('Issue text is too long (4096 characters maximum)')


async def on_support_ticket_subject_length_too_long(message: Message) -> None:
    await message.answer('Subject is too long (64 characters maximum)')


async def on_support_request_detail(
        callback_query: CallbackQuery,
        support_api_client: SupportAPIClient,
        callback_data: models.SupportTicketDetailCallbackData,
):
    support_request = await support_api_client.get_ticket_by_id(callback_data['ticket_id'])
    view = SupportRequestDetailView(support_request)
    await edit_message_by_view(callback_query.message, view)
    await callback_query.answer()


async def on_my_support_requests_list(message: Message, support_api_client: SupportAPIClient):
    support_requests = await support_api_client.get_user_tickets(message.from_user.id)
    view = SupportTicketsListView(support_requests)
    await answer_views(message, view)


async def on_support_ticket_issue_input(
        message: Message,
        state: FSMContext,
        support_api_client: SupportAPIClient,
) -> None:
    state_data = await state.get_data()
    ticket_create = models.SupportTicketCreate(
        issue=message.text,
        subject=state_data['subject'],
        user_telegram_id=message.from_user.id,
    )
    await state.finish()
    created_support_ticket = await support_api_client.create_ticket(ticket_create)
    await answer_views(message, SupportTicketCreatedView(created_support_ticket.id))


async def on_support_ticket_subject_input(message: Message, state: FSMContext) -> None:
    await state.update_data(subject=message.text)
    await NewSupportRequestStates.issue.set()
    await answer_views(message, RequireTicketIssueView())


async def on_new_support_request(message: Message, shop_info_api_client: ShopInfoAPIClient) -> None:
    support_rules = await shop_info_api_client.get_support_rules_info()
    view = AcceptSupportRulesView(support_rules)
    await answer_views(message, view)


async def on_support_rules_were_read(message: Message) -> None:
    await NewSupportRequestStates.subject.set()
    await answer_views(message, RequireTicketSubjectView())


async def on_support_menu(message: Message) -> None:
    await answer_views(message, SupportMenuView())


def register_handlers(dispatcher: Dispatcher) -> None:
    # Validators
    dispatcher.register_message_handler(
        on_support_ticket_subject_length_too_long,
        ~MessageLengthFilter(max_length=64),
        state=NewSupportRequestStates.subject,
    )
    dispatcher.register_message_handler(
        on_support_ticket_issue_length_too_long,
        ~MessageLengthFilter(max_length=4096),
        state=NewSupportRequestStates.issue,
    )

    dispatcher.register_message_handler(
        on_support_rules_were_read,
        Text('✅ I did'),
        state='*',
    )
    dispatcher.register_callback_query_handler(
        on_support_request_detail,
        SupportTicketDetailCallbackData().filter(),
        state='*',
    )
    dispatcher.register_message_handler(
        on_my_support_requests_list,
        Text('📓 Tickets'),
        state='*',
    )
    dispatcher.register_message_handler(
        on_new_support_request,
        Text('📋 Submit New Ticket'),
        state='*',
    )
    dispatcher.register_message_handler(
        on_support_ticket_subject_input,
        content_types=ContentType.TEXT,
        state=NewSupportRequestStates.subject,
    )
    dispatcher.register_message_handler(
        on_support_ticket_issue_input,
        content_types=ContentType.TEXT,
        state=NewSupportRequestStates.issue
    )
    dispatcher.register_message_handler(
        on_support_menu,
        Text('👨‍💻 Support'),
        state='*',
    )
