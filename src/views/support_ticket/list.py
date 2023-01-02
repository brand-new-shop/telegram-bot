from typing import Iterable

from aiogram.types import InlineKeyboardMarkup

import models
from views.base import View
from keyboards import SupportTicketsListMarkup

__all__ = ('SupportTicketsListView',)


class SupportTicketsListView(View):
    text = '📚 My Support Requests'

    def __init__(self, tickets: Iterable[models.SupportTicketPreview]):
        self.__tickets = tickets

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return SupportTicketsListMarkup(self.__tickets)
