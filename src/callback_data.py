from aiogram.utils.callback_data import CallbackData

import models

__all__ = ('ChooseSubjectCallbackData',)


class ChooseSubjectCallbackData(CallbackData):

    def __init__(self):
        super().__init__('choose-subject', 'support_subject_id')

    def parse(self, callback_data: str) -> models.ChooseSubjectCallbackData:
        callback_data = super().parse(callback_data)
        return {'support_subject_id': int(callback_data['support_subject_id'])}
