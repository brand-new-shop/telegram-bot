from aiogram.utils.callback_data import CallbackData

import models

__all__ = (
    'ChooseSubjectCallbackData',
    'SupportRequestDetailCallbackData',
    'CategoryDetailCallbackData',
)


class ChooseSubjectCallbackData(CallbackData):

    def __init__(self):
        super().__init__('choose-subject', 'support_subject_id')

    def parse(self, callback_data: str) -> models.ChooseSubjectCallbackData:
        callback_data = super().parse(callback_data)
        return {'support_subject_id': int(callback_data['support_subject_id'])}


class SupportRequestDetailCallbackData(CallbackData):

    def __init__(self):
        super().__init__('support-request-detail', 'support_request_id')

    def parse(self, callback_data: str) -> models.SupportRequestDetailCallbackData:
        callback_data = super().parse(callback_data)
        return {'support_request_id': int(callback_data['support_request_id'])}


class CategoryDetailCallbackData(CallbackData):

    def __init__(self):
        super().__init__('category-detail', 'category_id')

    def parse(self, callback_data: str):
        callback_data = super().parse(callback_data)
        return callback_data
