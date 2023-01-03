from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import models
from keyboards.buttons import RemoveMessageButton
from callback_data import CloseSupportTicketCallbackData

__all__ = ('SupportTicketDetailMarkup',)


class SupportTicketDetailMarkup(InlineKeyboardMarkup):

    def __init__(self, support_ticket: models.SupportTicket):
        super().__init__(row_width=1)
        if support_ticket.status != 'Closed':
            self.add(
                InlineKeyboardButton(
                    text='❌ Close ticket',
                    callback_data=CloseSupportTicketCallbackData().new(ticket_id=support_ticket.id),
                ),
            )
        self.insert(RemoveMessageButton())
