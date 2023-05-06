from collections.abc import Iterable
from decimal import Decimal

from aiogram.types import (
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton, InlineKeyboardButton,
)

from core.views import View
from info.views import ShopInfoView
from cart.models import OrdersStatistics
from products.models import OrderProduct, Order
from users.keyboards import MenuMarkup

__all__ = ('UserBalanceView', 'MenuView', 'ProfileView', 'AcceptRulesView')


class MenuView(View):
    text = '🔹 Main Menu 🔹'
    reply_markup = MenuMarkup()


class AcceptRulesView(ShopInfoView):
    reply_markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[[KeyboardButton('✅ Accept')]],
    )


class UserBalanceView(View):

    def __init__(self, user_balance_amount: Decimal):
        self.__user_balance_amount = user_balance_amount

    def get_text(self) -> str:
        return (
            f'⚖️ You current balance: ${self.__user_balance_amount}\n'
            'Do you want top up it?'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton(
                text='Top-up',
                callback_data='top-up',
            ),
        )
        return markup


class ProfileView(View):

    def __init__(
            self,
            telegram_id: int,
            username: str,
            orders_statistics: OrdersStatistics,
    ):
        self.__telegram_id = telegram_id
        self.__username = username
        self.__statistics = orders_statistics

    def get_text(self) -> str:
        username = self.__username or self.__telegram_id
        lines = [
            f'🙍‍♂ User: {username}',
            '➖➖➖➖➖➖➖➖➖➖',
            f'🛒 Number of purchases: {self.__statistics.total_count} pc(s).',
            f'💰 Total Amount: {self.__statistics.total_cost} $.',
        ]
        return '\n'.join(lines)
