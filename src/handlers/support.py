from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from shortcuts import answer_views
from views import SupportMenuView

__all__ = ('register_handlers',)


async def on_support_menu(message: Message):
    await answer_views(message, SupportMenuView())


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(on_support_menu, Text('👨‍💻 Support'), state='*')
