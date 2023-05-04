from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from cart.services import CartAPIClient
from cart.views import CartView
from cart import models
from cart.callback_data import ChangeProductQuantityInCartCallbackData
from core.services import HTTPClientFactory
from core.shortcuts import answer_views


async def on_change_product_quantity(
        callback_query: CallbackQuery,
        callback_data: models.HasProductIdAndQuantityTypedDict,
) -> None:
    print(callback_data)


async def on_show_cart(
        message: Message,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    async with closing_http_client_factory() as http_client:
        cart_api_client = CartAPIClient(http_client)
        cart_products = await cart_api_client.get_cart_products(
            telegram_id=message.from_user.id,
        )
    view = CartView(cart_products)
    await answer_views(message, view)


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_callback_query_handler(
        on_change_product_quantity,
        ChangeProductQuantityInCartCallbackData().filter(),
        state='*',
    )
    dispatcher.register_message_handler(
        on_show_cart,
        Text('🛒 My Shopping Cart'),
        state='*',
    )
