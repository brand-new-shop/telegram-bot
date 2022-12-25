from decimal import Decimal

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from models import UserProfileDTO, LastPurchaseDTO
from services.api import UsersAPIClient
from shortcuts import answer_views
from views import ProfileView

__all__ = ('register_handlers',)


async def on_profile(message: Message, users_api_client: UsersAPIClient):
    user_profile_dto = UserProfileDTO(
        message.from_user.id,
        message.from_user.username,
        1,
        Decimal('10.10'),
        [LastPurchaseDTO('Wine', 1, Decimal('10.10'))],
    )
    view = ProfileView(user_profile_dto)
    await answer_views(message, view)


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(on_profile, Text('📱 Profile'), state='*')
