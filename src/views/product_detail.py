from aiogram.types import MediaGroup, InputMediaPhoto, InlineKeyboardMarkup

import models
from keyboards import ProductDetailMarkup
from views.base import View

__all__ = ('ProductDetailView', 'ProductDetailWithPhotoView')


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

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return ProductDetailMarkup(self.__product)


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
        first_media_photo = [InputMediaPhoto(self.build_absolute_url(self.__product.picture_urls[0]),
                                             caption=self.get_text())]
        input_media_photos = [
            InputMediaPhoto(self.build_absolute_url(picture_url))
            for picture_url in self.__product.picture_urls[1:]
        ]
        return MediaGroup(first_media_photo + input_media_photos)

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return ProductDetailMarkup(self.__product)
