from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import models


class ProductDetailMarkup(InlineKeyboardMarkup):

    def __init__(self, product: models.Product):
        super().__init__()
        self.row(
            InlineKeyboardButton(
                text='🛍 Buy Now',
                callback_data='dev',
            ),
            InlineKeyboardButton(
                text='Add to Cart',
                callback_data='dev',
            )
        )
