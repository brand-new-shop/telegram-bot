import models
from keyboards import RemoveMessageMarkup
from views.base import View

__all__ = ('SupportRequestDetailView',)


class SupportRequestDetailView(View):
    reply_markup = RemoveMessageMarkup()

    def __init__(self, ticket: models.SupportTicket):
        self.__ticket = ticket

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
