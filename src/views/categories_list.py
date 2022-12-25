from typing import Iterable

from aiogram.types import InlineKeyboardMarkup

import models
from keyboards import CategoriesListMarkup
from views.base import View

__all__ = ('CategoriesListView',)


class CategoriesListView(View):
    text = '📂 All available categories'

    def __init__(self, categories: Iterable[models.Category]):
        self.__categories = categories

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return CategoriesListMarkup(self.__categories)
