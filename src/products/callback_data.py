from aiogram.utils.callback_data import CallbackData

from products import models

__all__ = (
    'CategoryDetailCallbackData',
    'ProductDetailCallbackData',
    'AddToCartCallbackData',
)


class CategoryDetailCallbackData(CallbackData):

    def __init__(self):
        super().__init__('category-detail', 'category_id')

    def parse(self, callback_data: str) -> models.ChooseCategoryCallbackData:
        callback_data = super().parse(callback_data)
        return {'category_id': int(callback_data['category_id'])}


class ProductDetailCallbackData(CallbackData):

    def __init__(self):
        super().__init__('product-detail', 'product_id')

    def parse(self, callback_data: str) -> models.ChooseProductCallbackData:
        callback_data = super().parse(callback_data)
        return {'product_id': int(callback_data['product_id'])}


class AddToCartCallbackData(CallbackData):

    def __init__(self):
        super().__init__('add-to-cart', 'product_id')

    def parse(self, callback_data: str) -> models.AddToCartCallbackData:
        callback_data = super().parse(callback_data)
        return {'product_id': int(callback_data['product_id'])}
