from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.buttons import RemoveMessageButton

__all__ = ('UserBalanceMarkup',)


class UserBalanceMarkup(InlineKeyboardMarkup):

    def __init__(self):
        super().__init__(row_width=1)
        self.add(
            InlineKeyboardButton('🔝 Top Up', callback_data='hello'),
            RemoveMessageButton(),
        )
