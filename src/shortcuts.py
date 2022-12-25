import contextlib

from aiogram.types import Message
from aiogram.utils.exceptions import TelegramAPIError

from views.base import View

__all__ = ('answer_views', 'edit_message_by_view')


async def answer_views(message: Message, *views: View):
    for view in views:
        with contextlib.suppress(TelegramAPIError):
            await message.answer(text=view.get_text(), reply_markup=view.get_reply_markup())


async def edit_message_by_view(message: Message, view: View):
    await message.edit_text(text=view.get_text(), reply_markup=view.get_reply_markup())
