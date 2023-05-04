from decimal import Decimal

from aiogram.types import (
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton, InlineKeyboardButton,
)

from core.views import View
from info.views import ShopInfoView
from users.models import UserProfileDTO
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

    def __init__(self, user_profile_dto: UserProfileDTO):
        self.__user_profile_dto = user_profile_dto

    def get_text(self) -> str:
        username = (
            f'@{self.__user_profile_dto.username}' if self.__user_profile_dto.username is not None
            else self.__user_profile_dto.telegram_id)
        lines = [
            f'🙍‍♂ User: {username}',
            '➖➖➖➖➖➖➖➖➖➖',
            f'🛒 Number of purchases: {self.__user_profile_dto.purchases_total_count} pc(s).',
            f'💰 Total Amount: {self.__user_profile_dto.purchases_total_price} $.',
        ]
        if self.__user_profile_dto.last_purchases:
            lines.append('➖➖➖➖➖➖➖➖➖➖')
            lines.append(
                f'📱 Last {len(self.__user_profile_dto.last_purchases)} purchases:')
            for purchase in self.__user_profile_dto.last_purchases:
                lines.append(
                    f'▫️ {purchase.product_name} | {purchase.quantity} pc(s) | ${purchase.total_price}')
        return '\n'.join(lines)
