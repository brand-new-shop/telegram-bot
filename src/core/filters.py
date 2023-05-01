from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

__all__ = ('MessageLengthFilter',)


class MessageLengthFilter(BoundFilter):
    key = 'message_length'

    def __init__(self, *, max_length: int):
        self.__max_length = max_length

    async def check(self, message: Message, *args) -> bool:
        message_text = (message.text if message.text is not None
                        else message.caption)
        return len(message_text) <= self.__max_length
