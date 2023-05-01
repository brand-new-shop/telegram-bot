from typing import Iterable

from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import MediaGroup, InputMediaPhoto

from products import models
from callback_data import CategoryDetailCallbackData, ProductDetailCallbackData
from core.views import View
from users.keyboards import RemoveMessageButton

__all__ = (
    'ProductDetailView',
    'ProductDetailWithPhotoView',
    'CategoriesListView',
    'CategoryMenuView',
)


class CategoryMenuView(View):

    def __init__(self, subcategories: Iterable[models.CategoryPreview],
                 products: Iterable[models.ProductPreview]):
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
        markup = InlineKeyboardMarkup(row_width=1)
        for subcategory in self.__subcategories:
            text = subcategory.name
            if subcategory.emoji_icon is not None:
                text = f'{subcategory.emoji_icon} {subcategory.name}'
            callback_data = CategoryDetailCallbackData().new(
                category_id=subcategory.id)
            markup.insert(InlineKeyboardButton(
                text=text,
                callback_data=callback_data,
            ))

        for product in self.__products:
            callback_data = ProductDetailCallbackData().new(
                product_id=product.id,
            )
            markup.insert(InlineKeyboardButton(
                text=product.name,
                callback_data=callback_data,
            ))
        markup.insert(RemoveMessageButton())
        return markup


class CategoriesListView(View):
    text = '📂 All available categories'

    def __init__(
            self,
            categories: Iterable[models.CategoryPreview] | None = None,
            products: Iterable[models.ProductPreview] | None = None,
    ):
        self.__categories = categories
        self.__products = products

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        for category in self.__categories:
            text = category.name if category.emoji_icon is None else f'{category.emoji_icon} {category.name}'
            button = InlineKeyboardButton(text,
                                          callback_data=CategoryDetailCallbackData().new(
                                              category_id=category.id))
            markup.insert(button)

        markup.insert(RemoveMessageButton())
        return markup


class ProductDetailView(View):

    def __init__(self, product: models.Product):
        self.__product = product

    def get_text(self) -> str:
        lines = [
            f'📓 Name: {self.__product.name}',
            f'📋 Description:\n {self.__product.description}',
            f'💳 Price: ${self.__product.price}.\n',
            f'📦 Available to purchase: {self.__product.stocks_count} pc(s)\n',
        ]
        if self.__product.stocks_count < 0:
            lines.append('❗️  The items are temporarily unavailable ❗️')
        return '\n'.join(lines)


class ProductDetailWithPhotoView(View):

    def __init__(self, server_base_url: str, product: models.Product):
        self.__server_base_url = server_base_url
        self.__product = product

    def get_text(self) -> str:
        lines = [
            f'📓 Name: {self.__product.name}',
            f'📋 Description:\n {self.__product.description}',
            f'💳 Price: ${self.__product.price}.\n',
            f'📦 Available to purchase: {self.__product.stocks_count} pc(s)\n',
        ]
        if self.__product.stocks_count < 0:
            lines.append('❗️  The items are temporarily unavailable ❗️')
        return '\n'.join(lines)

    def build_absolute_url(self, path: str) -> str:
        return f'{self.__server_base_url}/{path.removeprefix("/")}'

    def get_media_group(self) -> MediaGroup:
        first_media_photo = [InputMediaPhoto(
            self.build_absolute_url(self.__product.picture_urls[0]),
            caption=self.get_text())]
        input_media_photos = [
            InputMediaPhoto(self.build_absolute_url(picture_url))
            for picture_url in self.__product.picture_urls[1:]
        ]
        return MediaGroup(first_media_photo + input_media_photos)
