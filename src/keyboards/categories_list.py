from typing import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import models
from callback_data import CategoryDetailCallbackData
from keyboards.buttons import RemoveMessageButton

__all__ = ('CategoriesListMarkup',)


class CategoriesListMarkup(InlineKeyboardMarkup):

    def __init__(self, categories: Iterable[models.CategoryPreview]):
        super().__init__(row_width=1)
        for category in categories:
            text = category.name if category.emoji_icon is None else f'{category.emoji_icon} {category.name}'
            button = InlineKeyboardButton(text, callback_data=CategoryDetailCallbackData().new(category_id=category.id))
            self.insert(button)
        self.insert(RemoveMessageButton())
