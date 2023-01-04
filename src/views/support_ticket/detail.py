from typing import Iterable

from aiogram.types import InlineKeyboardMarkup

import models
from keyboards import SupportTicketDetailMarkup
from views.base import View

__all__ = ('SupportTicketDetailView',)


class SupportTicketDetailView(View):

    def __init__(self, ticket: models.SupportTicket, reply_ids: Iterable[int]):
        self.__ticket = ticket
        self.__reply_ids = reply_ids

    def get_text(self) -> str:
        lines = [
            f'🆔 Request number: #{self.__ticket.id}',
            '➖➖➖➖➖➖➖➖➖➖',
            f'📗 Request Subject: {self.__ticket.subject}',
            f'📋 Description: {self.__ticket.issue}',
            '➖➖➖➖➖➖➖➖➖➖',
        ]
        if self.__ticket.answer:
            lines.append(f'📧 Answer: {self.__ticket.answer}')
            lines.append('➖➖➖➖➖➖➖➖➖➖')
        lines.append(f'📱 Status: {self.__ticket.status}')
        return '\n'.join(lines)

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return SupportTicketDetailMarkup(self.__ticket, self.__reply_ids)
