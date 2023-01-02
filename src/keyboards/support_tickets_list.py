from typing import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import models
from keyboards.buttons import RemoveMessageButton
from callback_data import SupportTicketDetailCallbackData

__all__ = ('SupportTicketsListMarkup',)


class SupportTicketsListMarkup(InlineKeyboardMarkup):

    def __init__(self, tickets: Iterable[models.SupportTicketPreview]):
        super().__init__(row_width=1)
        self.add(
            *(
                InlineKeyboardButton(
                    text=f'{ticket.status} - #{ticket.id} - {ticket.subject}',
                    callback_data=SupportTicketDetailCallbackData().new(ticket_id=ticket.id),
                )
                for ticket in tickets
            ),
            RemoveMessageButton(),
        )
