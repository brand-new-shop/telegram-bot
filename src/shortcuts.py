import contextlib
import logging
import traceback

from aiogram.types import Message
from aiogram.utils.exceptions import TelegramAPIError

from views.base import View

__all__ = ('answer_views', 'edit_message_by_view')


async def answer_views(message: Message, *views: View) -> list[Message]:
    responses = []
    for view in views:
        media_group = view.get_media_group()
        if media_group is not None:
            responses.append(await message.answer_media_group(media_group))
        else:
            responses.append(await message.answer(text=view.get_text(), reply_markup=view.get_reply_markup()))
    return responses


async def edit_message_by_view(message: Message, view: View) -> Message:
    return await message.edit_text(text=view.get_text(), reply_markup=view.get_reply_markup())
