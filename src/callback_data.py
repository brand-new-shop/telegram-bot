from aiogram.utils.callback_data import CallbackData

import models

__all__ = (
    'SupportRequestDetailCallbackData',
    'CategoryDetailCallbackData',
    'ProductDetailCallbackData',
)


class SupportRequestDetailCallbackData(CallbackData):

    def __init__(self):
        super().__init__('support-request-detail', 'support_request_id')

    def parse(self, callback_data: str) -> models.SupportRequestDetailCallbackData:
        callback_data = super().parse(callback_data)
        return {'support_request_id': int(callback_data['support_request_id'])}


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
