from aiogram.utils.callback_data import CallbackData

import models

__all__ = (
    'SupportTicketDetailCallbackData',
    'CategoryDetailCallbackData',
    'ProductDetailCallbackData',
    'CloseSupportTicketCallbackData',
    'CreateReplyToTicketCallbackData',
    'ReplyToTicketDetailCallbackData',
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


class CreateReplyToTicketCallbackData(CallbackData):

    def __init__(self):
        super().__init__('create-reply-to-ticket', 'ticket_id')

    def parse(self, callback_data: str) -> models.ReplyToTicketCreateCallbackData:
        callback_data = super().parse(callback_data)
        return {'ticket_id': int(callback_data['ticket_id'])}


class ReplyToTicketDetailCallbackData(CallbackData):

    def __init__(self):
        super().__init__('reply-to-ticket-detail', 'ticket_reply_id')

    def parse(self, callback_data: str) -> models.ReplyToTicketDetailCallbackData:
        callback_data = super().parse(callback_data)
        return {'ticket_reply_id': int(callback_data['ticket_reply_id'])}
