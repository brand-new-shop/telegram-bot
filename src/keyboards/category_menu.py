from typing import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import models
from callback_data import CategoryDetailCallbackData, ProductDetailCallbackData
from keyboards.buttons import RemoveMessageButton

__all__ = ('CategoryMenuMarkup',)


class CategoryMenuMarkup(InlineKeyboardMarkup):

    def __init__(self, subcategories: Iterable[models.CategoryPreview], products: Iterable[models.ProductPreview]):
        super().__init__(row_width=1)
        for subcategory in subcategories:
            text = subcategory.name
            if subcategory.emoji_icon is not None:
                text = f'{subcategory.emoji_icon} {subcategory.name}'
            callback_data = CategoryDetailCallbackData().new(category_id=subcategory.id)
            self.insert(InlineKeyboardButton(text, callback_data=callback_data))

        for product in products:
            callback_data = ProductDetailCallbackData().new(product_id=product.id)
            self.insert(InlineKeyboardButton(product.name, callback_data=callback_data))

        self.insert(RemoveMessageButton())
