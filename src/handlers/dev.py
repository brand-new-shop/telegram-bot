from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

__all__ = ('register_handlers',)


async def on_developing_alert(callback_query: CallbackQuery) -> None:
    await callback_query.answer('👷‍♂️ In developing', show_alert=True)


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_callback_query_handler(
        on_developing_alert,
        Text('dev'),
        state='*',
    )
