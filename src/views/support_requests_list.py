from typing import Iterable

from aiogram.types import InlineKeyboardMarkup

import models
from views.base import View
from keyboards import SupportRequestsListMarkup

__all__ = ('SupportRequestsListView',)


class SupportRequestsListView(View):
    text = '📚 My Support Requests'

    def __init__(self, support_requests: Iterable[models.SupportRequestPreview]):
        self.__support_requests = support_requests

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return SupportRequestsListMarkup(self.__support_requests)
