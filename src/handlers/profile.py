import asyncio

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from models import UserProfileDTO
from services.api import UsersAPIClient
from shortcuts import answer_views
from views import ProfileView

__all__ = ('register_handlers',)


async def on_profile(message: Message, users_api_client: UsersAPIClient):
    orders, orders_statistics = await asyncio.gather(
        users_api_client.get_orders_by_telegram_id(message.from_user.id, limit=10, offset=0),
        users_api_client.get_orders_statistics(message.from_user.id),
    )
    user_profile_dto = UserProfileDTO(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        purchases_total_count=orders_statistics.orders_count,
        purchases_total_price=orders_statistics.orders_total_price,
        last_purchases=orders,
    )
    view = ProfileView(user_profile_dto)
    await answer_views(message, view)


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(on_profile, Text('📱 Profile'), state='*')
