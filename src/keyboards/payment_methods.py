from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.buttons import RemoveMessageButton

__all__ = ('PaymentMethodsMarkup',)


class PaymentMethodsMarkup(InlineKeyboardMarkup):

    def __init__(self):
        super().__init__(row_width=1)
        self.add(InlineKeyboardButton('Coinbase', callback_data='coinbase-top-up'))
        self.insert(RemoveMessageButton())
