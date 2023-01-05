from decimal import Decimal

from aiogram.types import InlineKeyboardMarkup

from views.base import View
from keyboards import CoinbasePaymentMarkup

__all__ = ('CoinbasePaymentView',)


class CoinbasePaymentView(View):

    def __init__(self, payment_amount: Decimal, payment_hosted_url: str):
        self.__payment_amount = payment_amount
        self.__payment_hosted_url = payment_hosted_url

    def get_text(self) -> str:
        return (
            "<b>Currency</b>: USD\n"
            f"<b>Amount: ${str(self.__payment_amount)}.</b>"
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return CoinbasePaymentMarkup(self.__payment_hosted_url)
