from typing import Iterable

from aiogram.types import InlineKeyboardMarkup

import models
from keyboards import ChooseSubjectMarkup
from views.base import View

__all__ = ('ChooseSubjectView',)


class ChooseSubjectView(View):
    text = '📋 New Support Request'

    def __init__(self, support_subjects: Iterable[models.SupportSubject]):
        self.__support_subjects = support_subjects

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return ChooseSubjectMarkup(self.__support_subjects)
