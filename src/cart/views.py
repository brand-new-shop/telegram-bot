from collections.abc import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from cart import models
from cart.callback_data import ChangeProductQuantityInCartCallbackData
from core.views import View
from products.callback_data import ProductDetailCallbackData
from products.models import Product

__all__ = (
    'CartView',
    'PaymentMethodsView',
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
                callback_data='start-order-processing',
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


class PaymentMethodsView(View):

    def __init__(self, balance_only_products: Iterable[Product] | None = None):
        self.__balance_only_products = tuple(balance_only_products)

    def get_text(self) -> str:
        if self.__balance_only_products:
            text = ['Since the following products are <u>balance only</u>,'
                    ' you can pay for your order only using your balance:']
            for product in self.__balance_only_products:
                text.append(f'📍 {product.name}')
        else:
            text = ['Select a payment method']
        return '\n'.join(text)

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup(row_width=1)
        if self.__balance_only_products:
            markup.insert(
                InlineKeyboardButton(
                    text='Pay',
                    callback_data='pay-via-balance',
                ),
            )
        else:
            markup.add(
                InlineKeyboardButton(
                    text='Balance',
                    callback_data='pay-via-balance',
                ),
                InlineKeyboardButton(
                    text='Coinbase',
                    callback_data='pay-via-coinbase',
                ),

            )
        return markup
