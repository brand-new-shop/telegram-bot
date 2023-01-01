from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ContentType, CallbackQuery

import exceptions
import models
from models import SupportRequestCreate
from services.api import SupportAPIClient, ShopInfoAPIClient
from shortcuts import answer_views, edit_message_by_view
from views import (
    SupportMenuView,
    SupportRequestCreatedView,
    ChooseSubjectView,
    SupportRequestsListView,
    SupportRequestDetailView,
    AcceptSupportRulesView,
)
from states import NewSupportSubjectStates, NewSupportRequestStates
from callback_data import ChooseSubjectCallbackData, SupportRequestDetailCallbackData

__all__ = ('register_handlers',)


async def on_support_request_detail(
        callback_query: CallbackQuery,
        support_api_client: SupportAPIClient,
        callback_data: models.SupportRequestDetailCallbackData,
):
    support_request = await support_api_client.get_request_by_id(callback_data['support_request_id'])
    view = SupportRequestDetailView(support_request)
    await edit_message_by_view(callback_query.message, view)
    await callback_query.answer()


async def on_my_support_requests_list(message: Message, support_api_client: SupportAPIClient):
    support_requests = await support_api_client.get_requests_by_user_telegram_id(message.from_user.id)
    view = SupportRequestsListView(support_requests)
    await answer_views(message, view)


async def on_input_support_request_issue(
        message: Message,
        support_api_client: SupportAPIClient,
        state: FSMContext,
) -> None:
    state_data = await state.get_data()
    await state.finish()
    subject_id = state_data['support_subject_id']
    support_request_create_dto = SupportRequestCreate(
        user_telegram_id=message.from_user.id,
        issue=message.text,
        subject_id=subject_id,
    )
    created_support_request = await support_api_client.create_request(support_request_create_dto)
    await answer_views(message, SupportRequestCreatedView(created_support_request.id))


async def on_choose_support_subject(
        callback_query: CallbackQuery,
        callback_data: models.ChooseSubjectCallbackData,
        state: FSMContext,
) -> None:
    await state.update_data(support_subject_id=callback_data['support_subject_id'])
    await NewSupportRequestStates.issue.set()
    await callback_query.message.edit_text('📋 Describe your problem/question')
    await callback_query.answer()


async def on_new_support_request(message: Message, support_api_client: SupportAPIClient) -> None:
    subjects = await support_api_client.get_subjects()
    await NewSupportRequestStates.subject.set()
    await answer_views(message, ChooseSubjectView(subjects))


async def on_new_support_subject_name_input(
        message: Message,
        support_api_client: SupportAPIClient,
        state: FSMContext,
) -> None:
    if len(message.text) > 64:
        await message.reply('Too long name')
        return
    try:
        await support_api_client.create_subject(message.text)
    except exceptions.ServerAPIError:
        await message.reply('❌ Could not create new support subject')
        return
    await state.finish()
    await message.answer('✅ Ready')


async def on_new_support_subject(message: Message) -> None:
    await NewSupportSubjectStates.name.set()
    await message.answer('🛟 Input support subject')


async def on_support_rules_were_read(message: Message) -> None:
    await answer_views(message, SupportMenuView())


async def on_support_menu(message: Message, shop_info_api_client: ShopInfoAPIClient) -> None:
    support_rules = await shop_info_api_client.get_support_rules_info()
    view = AcceptSupportRulesView(support_rules)
    await answer_views(message, view)


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(
        on_support_rules_were_read,
        Text('✅ I did'),
        state='*',
    )
    dispatcher.register_callback_query_handler(
        on_support_request_detail,
        SupportRequestDetailCallbackData().filter(),
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
    dispatcher.register_callback_query_handler(
        on_choose_support_subject,
        ChooseSubjectCallbackData().filter(),
        state=NewSupportRequestStates.subject,
    )
    dispatcher.register_message_handler(
        on_input_support_request_issue,
        content_types=ContentType.TEXT,
        state=NewSupportRequestStates.issue
    )
    dispatcher.register_message_handler(
        on_new_support_subject_name_input,
        content_types=ContentType.TEXT,
        state=NewSupportSubjectStates.name,
    )
    dispatcher.register_message_handler(
        on_new_support_subject,
        Text('🆘 New Support Subject'),
        state='*',
    )
    dispatcher.register_message_handler(
        on_support_menu,
        Text('👨‍💻 Support'),
        state='*',
    )
