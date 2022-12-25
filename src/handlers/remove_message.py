from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import TelegramAPIError

__all__ = ('register_handlers',)


async def on_remove_message(callback_query: CallbackQuery):
    try:
        await callback_query.message.delete()
    except TelegramAPIError:
        pass
    await callback_query.answer()


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_callback_query_handler(on_remove_message, Text('remove-message'), state='*')
