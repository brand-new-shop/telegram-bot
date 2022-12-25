import contextlib

from aiogram.types import Message
from aiogram.utils.exceptions import TelegramAPIError

from views.base import View

__all__ = ('answer_views',)


async def answer_views(message: Message, *views: View):
    for view in views:
        with contextlib.suppress(TelegramAPIError):
            await message.answer(text=view.get_text(), reply_markup=view.get_reply_markup())
