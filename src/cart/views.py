from collections.abc import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from cart import models
from cart.callback_data import ChangeProductQuantityInCartCallbackData
from core.views import View
from products.callback_data import ProductDetailCallbackData

__all__ = (
    'CartView',
)


class CartView(View):

    def __init__(self, cart_products: Iterable[models.CartProduct]):
        self.__cart_products = tuple(cart_products)

    def get_text(self) -> str:
        if not self.__cart_products:
            return '🛒 Your cart is empty'
        total_cost = sum(
            product.product_price * product.quantity
            for product in self.__cart_products
        )
        return f'Total cost of items: ${total_cost}'

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        for cart_product in self.__cart_products:
            markup.row(
                InlineKeyboardButton(
                    text=cart_product.product_name,
                    callback_data=ProductDetailCallbackData().new(
                        product_id=cart_product.product_id,
                    ),
                ),
                InlineKeyboardButton(
                    text='+',
                    callback_data=ChangeProductQuantityInCartCallbackData().new(
                        cart_product_id=cart_product.id,
                        product_id=cart_product.product_id,
                        quantity=cart_product.quantity + 1,
                    ),
                ),
                InlineKeyboardButton(
                    text=str(cart_product.quantity),
                    callback_data='g',
                ),
                InlineKeyboardButton(
                    text='-',
                    callback_data=ChangeProductQuantityInCartCallbackData().new(
                        cart_product_id=cart_product.id,
                        product_id=cart_product.product_id,
                        quantity=cart_product.quantity - 1,
                    ),
                ),
                InlineKeyboardButton(
                    text='❌',
                    callback_data='g',
                ),
            )
        markup.row(
            InlineKeyboardButton(
                text='🛒 Continue Shopping',
                callback_data='to-categories',
            ),
        )
        markup.row(
            InlineKeyboardButton(
                text='🛍 Buy Now',
                callback_data='payment-methods',
            ),
        )
        if self.__cart_products:
            markup.row(
                InlineKeyboardButton(
                    text='🧹 Empty Cart',
                    callback_data='empty-cart',
                ),
            )
        return markup
