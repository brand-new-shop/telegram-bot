import models
from views.base import View

__all__ = ('ReplyToTicketDetailView',)


class ReplyToTicketDetailView(View):

    def __init__(self, reply_to_ticket: models.ReplyToTicket):
        self.__reply_to_ticket = reply_to_ticket

    def get_text(self) -> str:
        lines = [
            f'🆔 Reply to ticket #{self.__reply_to_ticket.ticket.id}',
            '➖➖➖➖➖➖➖➖➖➖',
            f'📋 Description: \n{self.__reply_to_ticket.issue}'
        ]
        if self.__reply_to_ticket.answer:
            lines.append('➖➖➖➖➖➖➖➖➖➖')
            lines.append(f'Answer: \n{self.__reply_to_ticket.answer}')
        return '\n'.join(lines)
