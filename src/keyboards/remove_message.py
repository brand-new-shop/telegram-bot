from aiogram.types import InlineKeyboardMarkup

from keyboards.buttons import RemoveMessageButton

__all__ = ('RemoveMessageMarkup',)


class RemoveMessageMarkup(InlineKeyboardMarkup):

    def __init__(self):
        super().__init__()
        self.add(RemoveMessageButton())
