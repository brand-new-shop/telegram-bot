import asyncio

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import Message
from aiogram.utils.exceptions import TelegramAPIError

from core import exceptions
from core.services import HTTPClientFactory
from core.shortcuts import answer_views
from info.services import ShopInfoAPIClient
from info.views import ShopInfoView
from users.models import UserProfileDTO
from users.services import UsersAPIClient
from users.views import MenuView, AcceptRulesView, ProfileView

__all__ = ('register_handlers',)


async def on_profile(message: Message, users_api_client: UsersAPIClient):
    orders, orders_statistics = await asyncio.gather(
        users_api_client.get_orders_by_telegram_id(message.from_user.id,
                                                   limit=10, offset=0),
        users_api_client.get_orders_statistics(message.from_user.id),
    )
    user_profile_dto = UserProfileDTO(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        purchases_total_count=orders_statistics.orders_count,
        purchases_total_price=orders_statistics.orders_total_price,
        last_purchases=orders,
    )
    view = ProfileView(user_profile_dto)
    await answer_views(message, view)


async def on_remove_message(callback_query: CallbackQuery):
    try:
        await callback_query.message.delete()
    except TelegramAPIError:
        pass
    await callback_query.answer()


async def on_rules(
        message: Message,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    async with closing_http_client_factory() as http_client:
        shop_info_api_client = ShopInfoAPIClient(http_client)
        try:
            faq = await shop_info_api_client.get_rules_info()
        except exceptions.ShopInfoNotFoundError:
            await message.answer('Rules')
        else:
            await answer_views(message, ShopInfoView(faq))


async def on_faq(
        message: Message,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    async with closing_http_client_factory() as http_client:
        shop_info_api_client = ShopInfoAPIClient(http_client)
        try:
            faq = await shop_info_api_client.get_faq_info()
        except exceptions.ShopInfoNotFoundError:
            await message.answer('FAQ')
        else:
            await answer_views(message, ShopInfoView(faq))


async def on_accept_rules(
        message: Message,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    async with closing_http_client_factory() as http_client:
        users_api_client = UsersAPIClient(http_client)
        try:
            await users_api_client.create(
                telegram_id=message.from_user.id,
                username=message.from_user.username
            )
        except exceptions.ServerAPIError:
            return
    await answer_views(message, MenuView())


async def on_start(
        message: Message,
        closing_http_client_factory: HTTPClientFactory,
        state: FSMContext,
) -> None:
    async with closing_http_client_factory() as http_client:
        users_api_client = UsersAPIClient(http_client)
        shop_info_api_client = ShopInfoAPIClient(http_client)
        try:
            await users_api_client.get_by_telegram_id(message.from_user.id)
        except exceptions.UserNotFoundError:
            markup = ReplyKeyboardMarkup(
                resize_keyboard=True,
                keyboard=[[KeyboardButton('✅ Accept')]],
            )
            try:
                shop_info = await shop_info_api_client.get_rules_info()
            except exceptions.ShopInfoNotFoundError:
                await message.answer('Rules', reply_markup=markup)
            else:
                await answer_views(message, AcceptRulesView(shop_info))
            return
    await state.finish()
    await answer_views(message, MenuView())


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(
        on_profile,
        Text('📱 Profile'),
        state='*',
    )
    dispatcher.register_message_handler(
        on_start,
        CommandStart() | Text('⬅️ Back'),
        state='*',
    )
    dispatcher.register_message_handler(
        on_accept_rules,
        Text('✅ Accept'),
        state='*',
    )
    dispatcher.register_message_handler(
        on_faq,
        Text('ℹ️ FAQ'),
        state='*',
    )
    dispatcher.register_message_handler(
        on_rules,
        Text('📗 Rules'),
        state='*',
    )
    dispatcher.register_callback_query_handler(
        on_remove_message,
        Text('remove-message'),
        state='*',
    )
