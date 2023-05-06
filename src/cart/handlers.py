from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from cart.services import CartAPIClient
from cart.views import CartView, PaymentMethodsView
from cart import models
from cart.callback_data import ChangeProductQuantityInCartCallbackData
from core.services import HTTPClientFactory
from core.shortcuts import answer_views, edit_message_by_view
from products.services import ProductsAPIClient
from users.services import UsersAPIClient


async def on_select_balance_as_payment_method(
        callback_query: CallbackQuery,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    async with closing_http_client_factory() as http_client:
        users_api_client = UsersAPIClient(http_client)
        cart_api_client = CartAPIClient(http_client)
        user = await users_api_client.get_by_telegram_id(
            telegram_id=callback_query.from_user.id,
        )
        cart_products = await cart_api_client.get_cart_products(
            telegram_id=callback_query.from_user.id,
        )
        if not cart_products:
            await callback_query.answer(
                'Your shopping cart is empty',
                show_alert=True,
            )
            return

        cart_total_cost = sum(
            cart_product.quantity * cart_product.product_price
            for cart_product in cart_products
        )
        if cart_total_cost > user.balance:
            missing_amount = cart_total_cost - user.balance
            text = (
                'You do not have enough balance on your account.'
                f' you need an additional ${missing_amount}'
                ' to complete the order'
            )
            await callback_query.answer(text, show_alert=True)
            return

        order = await cart_api_client.create_order(
            telegram_id=callback_query.from_user.id,
            payment_method='balance',
        )
    await callback_query.message.edit_text('Order successfully created')


async def on_start_order_processing(
        callback_query: CallbackQuery,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    async with closing_http_client_factory() as http_client:
        cart_api_client = CartAPIClient(http_client)
        products_api_client = ProductsAPIClient(http_client)

        cart_products = await cart_api_client.get_cart_products(
            telegram_id=callback_query.from_user.id,
        )
        products = []
        for cart_product in cart_products:
            products.append(
                await products_api_client.get_product_by_id(
                    product_id=cart_product.product_id,
                )
            )
    balance_only_products = [
        product for product in products
        if product.is_balance_only
    ]
    view = PaymentMethodsView(balance_only_products)
    await answer_views(callback_query.message, view)


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
        on_select_balance_as_payment_method,
        Text('pay-via-balance'),
        state='*',
    )
    dispatcher.register_callback_query_handler(
        on_start_order_processing,
        Text('start-order-processing'),
        state='*',
    )
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
