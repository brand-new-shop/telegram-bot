import asyncio

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ContentType, CallbackQuery, Update

import exceptions
import models
from callback_data import (
    SupportTicketDetailCallbackData,
    CloseSupportTicketCallbackData,
    CreateReplyToTicketCallbackData,
    ReplyToTicketDetailCallbackData
)
from filters import MessageLengthFilter
from services.api import SupportAPIClient, ShopInfoAPIClient
from shortcuts import answer_views, edit_message_by_view
from states import NewSupportRequestStates, NewReplyToTicketStates
from views import (
    SupportMenuView,
    SupportTicketCreatedView,
    RequireTicketIssueView,
    SupportTicketsListView,
    SupportTicketDetailView,
    AcceptSupportRulesView,
    RequireTicketSubjectView,
    SupportTicketRateLimitExceededView,
    ReplyToTicketDetailView,
)

__all__ = ('register_handlers',)


async def on_support_tickets_not_found_error(
        update: Update,
        exception: exceptions.SupportTicketsNotFoundError,
) -> bool:
    await update.message.answer('You haven\'t created any ticket')
    return True


# Error handlers
async def on_support_ticket_creation_rate_limit_exceeded_error(
        update: Update,
        exception: exceptions.SupportTicketCreationRateLimitExceededError,
) -> bool:
    await Dispatcher.get_current().current_state().finish()
    view = SupportTicketRateLimitExceededView(exception.seconds_to_wait)
    await answer_views(update.message, view)
    return True


# Validators
async def on_reply_to_ticket_issue_length_too_long(message: Message) -> None:
    await message.answer('Issue text is too long (4096 characters maximum)')


async def on_support_ticket_issue_length_too_long(message: Message) -> None:
    await message.answer('Issue text is too long (4096 characters maximum)')


async def on_support_ticket_subject_length_too_long(message: Message) -> None:
    await message.answer('Subject is too long (64 characters maximum)')


async def on_close_ticket(
        callback_query: CallbackQuery,
        support_api_client: SupportAPIClient,
        callback_data: models.SupportTicketDetailCallbackData,
) -> None:
    ticket_id = callback_data['ticket_id']
    is_closed = await support_api_client.close_ticket_by_id(ticket_id)
    if not is_closed:
        await callback_query.answer('Unable to close the ticket', show_alert=True)
        return
    support_ticket, ticket_reply_ids, _ = await asyncio.gather(
        support_api_client.get_ticket_by_id(ticket_id),
        support_api_client.get_ticket_reply_ids(callback_data['ticket_id']),
        callback_query.answer('You have closed the ticket', show_alert=True),
    )
    view = SupportTicketDetailView(support_ticket, ticket_reply_ids)
    await edit_message_by_view(callback_query.message, view)


async def on_create_reply_to_ticket_issue_input(
        message: Message,
        support_api_client: SupportAPIClient,
        state: FSMContext,
) -> None:
    state_data = await state.get_data()
    await state.finish()
    ticket_id = state_data['ticket_id']
    await support_api_client.create_reply_to_ticket(ticket_id, message.text)
    await message.answer('Your reply added to this active request')


async def on_create_reply_to_ticket(
        callback_query: CallbackQuery,
        callback_data: models.ReplyToTicketCreateCallbackData,
        state: FSMContext,
) -> None:
    await NewReplyToTicketStates.issue.set()
    await state.update_data(ticket_id=callback_data['ticket_id'])
    await callback_query.message.answer('Please enter more details or comments related to this active request:')
    await callback_query.answer()


async def on_ticket_reply_detail(
        callback_query: CallbackQuery,
        support_api_client: SupportAPIClient,
        callback_data: models.ReplyToTicketDetailCallbackData,
) -> None:
    ticket_reply_id = callback_data['ticket_reply_id']
    reply_to_ticket = await support_api_client.get_reply_to_ticket(ticket_reply_id)
    view = ReplyToTicketDetailView(reply_to_ticket)
    await answer_views(callback_query.message, view)
    await callback_query.answer()


async def on_support_ticket_detail(
        callback_query: CallbackQuery,
        support_api_client: SupportAPIClient,
        callback_data: models.SupportTicketDetailCallbackData,
) -> None:
    support_ticket, ticket_reply_ids = await asyncio.gather(
        support_api_client.get_ticket_by_id(callback_data['ticket_id']),
        support_api_client.get_ticket_reply_ids(callback_data['ticket_id']),
    )
    view = SupportTicketDetailView(support_ticket, ticket_reply_ids)
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
    try:
        support_rules = await shop_info_api_client.get_support_rules_info()
    except exceptions.ShopInfoNotFoundError:
        support_rules = models.ShopInfo(key='support_rules', value='support_rules')
    view = AcceptSupportRulesView(support_rules)
    await answer_views(message, view)


async def on_support_rules_were_read(message: Message) -> None:
    await NewSupportRequestStates.subject.set()
    await answer_views(message, RequireTicketSubjectView())


async def on_support_menu(message: Message) -> None:
    await answer_views(message, SupportMenuView())


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_errors_handler(
        on_support_tickets_not_found_error,
        exception=exceptions.SupportTicketsNotFoundError,
    )
    dispatcher.register_errors_handler(
        on_support_ticket_creation_rate_limit_exceeded_error,
        exception=exceptions.SupportTicketCreationRateLimitExceededError,
    )

    # Validators
    dispatcher.register_message_handler(
        on_reply_to_ticket_issue_length_too_long,
        ~MessageLengthFilter(max_length=4096),
        state=NewReplyToTicketStates.issue,
    )
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

    dispatcher.register_callback_query_handler(
        on_ticket_reply_detail,
        ReplyToTicketDetailCallbackData().filter(),
        state='*',
    )
    dispatcher.register_message_handler(
        on_create_reply_to_ticket_issue_input,
        state=NewReplyToTicketStates.issue,
    )
    dispatcher.register_callback_query_handler(
        on_create_reply_to_ticket,
        CreateReplyToTicketCallbackData().filter(),
        state='*',
    )
    dispatcher.register_callback_query_handler(
        on_close_ticket,
        CloseSupportTicketCallbackData().filter(),
        state='*',
    )
    dispatcher.register_message_handler(
        on_support_rules_were_read,
        Text('✅ I did'),
        state='*',
    )
    dispatcher.register_callback_query_handler(
        on_support_ticket_detail,
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
