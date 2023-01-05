from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

__all__ = ('CoinbasePaymentMarkup',)


class CoinbasePaymentMarkup(InlineKeyboardMarkup):

    def __init__(self, payment_hosted_url: str):
        super().__init__()
        self.add(InlineKeyboardButton(text='🧾 Pay', url=payment_hosted_url))
