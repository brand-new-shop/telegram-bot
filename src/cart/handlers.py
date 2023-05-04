from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from cart.services import CartAPIClient
from cart.views import CartView
from cart import models
from cart.callback_data import ChangeProductQuantityInCartCallbackData
from core.services import HTTPClientFactory
from core.shortcuts import answer_views, edit_message_by_view
from products.services import ProductsAPIClient


async def on_empty_cart(
        callback_query: CallbackQuery,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    async with closing_http_client_factory() as http_client:
        cart_api_client = CartAPIClient(http_client)
        cart_products = await cart_api_client.get_cart_products(
            telegram_id=callback_query.from_user.id,
        )
        for cart_product in cart_products:
            await cart_api_client.delete_cart_product(cart_product.id)
        await callback_query.answer(
            'All items in your cart have been removed',
            show_alert=True,
        )
        cart_products = await cart_api_client.get_cart_products(
            telegram_id=callback_query.from_user.id,
        )
    view = CartView(cart_products)
    await edit_message_by_view(callback_query.message, view)


async def on_change_product_quantity(
        callback_query: CallbackQuery,
        callback_data: models.ChangeProductQuantityInCartTypedDict,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    cart_product_id = callback_data['cart_product_id']
    quantity = callback_data['quantity']
    product_id = callback_data['product_id']

    async with closing_http_client_factory() as http_client:
        cart_api_client = CartAPIClient(http_client)
        products_api_client = ProductsAPIClient(http_client)
        product = await products_api_client.get_product_by_id(product_id)
        cart_product = await cart_api_client.get_cart_product(cart_product_id)
        cart_product_quantity_change = quantity - cart_product.quantity
        if cart_product_quantity_change > product.stocks_count:
            await callback_query.answer('Not enough stocks', show_alert=True)
            return
        if quantity <= 0:
            await cart_api_client.delete_cart_product(cart_product_id)
        else:
            await cart_api_client.update_cart_product_quantity(
                cart_product_id, quantity
            )
            await callback_query.answer(
                'You have updated the quantity of the item in the cart'
            )
        cart_products = await cart_api_client.get_cart_products(
            telegram_id=callback_query.from_user.id,
        )
    view = CartView(cart_products)
    await edit_message_by_view(callback_query.message, view)


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
        on_empty_cart,
        Text('empty-cart'),
        state='*',
    )
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
