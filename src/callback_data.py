from aiogram.utils.callback_data import CallbackData

import models

__all__ = (
    'SupportTicketDetailCallbackData',
    'CategoryDetailCallbackData',
    'ProductDetailCallbackData',
    'CloseSupportTicketCallbackData',
)


class SupportTicketDetailCallbackData(CallbackData):

    def __init__(self):
        super().__init__('support-ticket-detail', 'ticket_id')

    def parse(self, callback_data: str) -> models.SupportTicketDetailCallbackData:
        callback_data = super().parse(callback_data)
        return {'ticket_id': int(callback_data['ticket_id'])}


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


class CloseSupportTicketCallbackData(CallbackData):

    def __init__(self):
        super().__init__('close-ticket', 'ticket_id')

    def parse(self, callback_data: str) -> models.CloseSupportTicketCallbackData:
        callback_data = super().parse(callback_data)
        return {'ticket_id': int(callback_data['ticket_id'])}
