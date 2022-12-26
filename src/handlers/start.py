from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.types import Message

import exceptions
from services.api.users import UsersAPIClient
from shortcuts import answer_views
from views import AcceptRulesView, MenuView

__all__ = ('register_handlers',)


async def on_rules(message: Message) -> None:
    await message.answer('Rules')


async def on_faq(message: Message) -> None:
    await message.answer('FAQ')


async def on_accept_rules(message: Message, users_api_client: UsersAPIClient) -> None:
    try:
        await users_api_client.create(message.from_user.id, message.from_user.username)
    except exceptions.ServerAPIError:
        return
    await answer_views(message, MenuView())


async def on_start(message: Message, users_api_client: UsersAPIClient, state: FSMContext) -> None:
    try:
        await users_api_client.get_by_telegram_id(message.from_user.id)
    except exceptions.UserNotFoundError:
        await answer_views(message, AcceptRulesView())
        return
    except exceptions.ServerAPIError:
        return
    await state.finish()
    await answer_views(message, MenuView())


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(on_start, CommandStart(), state='*')
    dispatcher.register_message_handler(on_start, Text('⬅️ Back'), state='*')
    dispatcher.register_message_handler(on_accept_rules, Text('✅ Accept'), state='*')
    dispatcher.register_message_handler(on_faq, Text('ℹ️ FAQ'), state='*')
    dispatcher.register_message_handler(on_rules, Text('📗 Rules'), state='*')
