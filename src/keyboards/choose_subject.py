from typing import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import models
from keyboards.buttons import RemoveMessageButton
from callback_data import ChooseSubjectCallbackData

__all__ = ('ChooseSubjectMarkup',)


class ChooseSubjectMarkup(InlineKeyboardMarkup):

    def __init__(self, subjects: Iterable[models.SupportSubject]):
        super().__init__(row_width=1)
        self.add(
            *(
                InlineKeyboardButton(
                    text=subject.name,
                    callback_data=ChooseSubjectCallbackData().new(support_subject_id=subject.id),
                )
                for subject in subjects
            ),
            RemoveMessageButton(),
        )
