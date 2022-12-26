from typing import Iterable

from aiogram.types import InlineKeyboardMarkup

import models
from views.base import View
from keyboards import CategoryMenuMarkup

__all__ = ('CategoryMenuView',)


class CategoryMenuView(View):

    def __init__(self, subcategories: Iterable[models.CategoryPreview], products: Iterable[models.ProductPreview]):
        self.__subcategories = tuple(subcategories)
        self.__products = tuple(products)

    def get_text(self) -> str:
        if self.__subcategories and self.__products:
            return '📂 All available categories and products'
        elif self.__subcategories:
            return '📂 All available categories'
        elif self.__products:
            return '📂 All available products'
        return '😔 Oh, there is nothing here ('

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return CategoryMenuMarkup(self.__subcategories, self.__products)
