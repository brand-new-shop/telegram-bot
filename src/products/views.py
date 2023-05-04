from typing import Iterable

from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import MediaGroup, InputMediaPhoto

from core.views import View
from products import models
from products.callback_data import (
    CategoryDetailCallbackData,
    ProductDetailCallbackData,
)
from users.keyboards import RemoveMessageButton

__all__ = (
    'ProductDetailView',
    'ProductDetailPhotosView',
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

    def __init__(
            self,
            categories: Iterable[models.CategoryPreview] | None = None,
            products: Iterable[models.ProductPreview] | None = None,
    ):
        self.__categories = categories
        self.__products = products

    def get_text(self) -> str:
        if self.__categories and self.__products:
            return '📂 All available categories and products'
        if self.__categories:
            return '📂 All available categories'
        if self.__products:
            return '📂 All available products'
        return '😔 There\'s nothing here'

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup(row_width=1)

        if self.__categories is not None:
            for category in self.__categories:
                text = (category.name if category.emoji_icon is None
                        else f'{category.emoji_icon} {category.name}')
                button = InlineKeyboardButton(
                    text=text,
                    callback_data=CategoryDetailCallbackData().new(
                        category_id=category.id,
                    ),
                )
                markup.insert(button)

        if self.__products is not None:
            for product in self.__products:
                button = InlineKeyboardButton(
                    text=product.name,
                    callback_data=ProductDetailCallbackData().new(
                        product_id=product.id,
                    ),
                )
                markup.insert(button)

        markup.insert(RemoveMessageButton())
        return markup


class ProductDetailView(View):

    def __init__(self, product: models.Product):
        self._product = product

    def get_text(self) -> str:
        lines = [
            f'📓 Name: {self._product.name}',
            f'📋 Description:\n {self._product.description}',
            f'💳 Price: ${self._product.price}.\n',
            f'📦 Available to purchase: {self._product.stocks_count} pc(s)\n',
        ]
        if self._product.stocks_count < 0:
            lines.append('❗️  The items are temporarily unavailable ❗️')
        return '\n'.join(lines)

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton(
                text='🛍 Buy Now',
                callback_data='dev',
            ),
            InlineKeyboardButton(
                text='🛒 Add to Cart',
                callback_data='dev',
            )
        )
        return markup


class ProductDetailPhotosView(View):

    def __init__(self, product: models.Product):
        self._product = product

    def get_media_group(self) -> MediaGroup:
        input_media_photos = [
            InputMediaPhoto(picture_url)
            for picture_url in self._product.picture_urls
        ]
        return MediaGroup(input_media_photos)
