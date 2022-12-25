from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from services.api import UsersAPIClient
from views import UserBalanceView

from shortcuts import answer_views

__all__ = ('register_handlers',)


async def on_user_balance(message: Message, users_api_client: UsersAPIClient) -> None:
    user = await users_api_client.get_by_telegram_id(message.from_user.id)
    view = UserBalanceView(user.balance)
    await answer_views(message, view)


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(on_user_balance, Text('💲 Balance'), state='*')
