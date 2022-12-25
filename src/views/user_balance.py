from decimal import Decimal

from aiogram.types import InlineKeyboardMarkup

from keyboards import UserBalanceMarkup
from views.base import View

__all__ = ('UserBalanceView',)


class UserBalanceView(View):

    def __init__(self, user_balance_amount: Decimal):
        self.__user_balance_amount = user_balance_amount

    def get_text(self) -> str:
        return (
            f'⚖️ You current balance: ${self.__user_balance_amount}\n'
            'Do you want top up it?'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return UserBalanceMarkup()
