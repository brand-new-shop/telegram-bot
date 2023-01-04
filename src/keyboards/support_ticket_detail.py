from typing import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import models
from keyboards.buttons import RemoveMessageButton
from callback_data import (
    CloseSupportTicketCallbackData,
    CreateReplyToTicketCallbackData,
    ReplyToTicketDetailCallbackData,
)

__all__ = ('SupportTicketDetailMarkup',)


class SupportTicketDetailMarkup(InlineKeyboardMarkup):

    def __init__(self, support_ticket: models.SupportTicket, reply_ids: Iterable[int]):
        super().__init__(row_width=1)
        for i, reply_id in enumerate(reply_ids, start=1):
            self.insert(InlineKeyboardButton(
                text=f'Reply #{i}',
                callback_data=ReplyToTicketDetailCallbackData().new(ticket_reply_id=reply_id),
            ))

        if support_ticket.status != 'Closed':
            self.row(
                InlineKeyboardButton(
                    text='➕ Reply',
                    callback_data=CreateReplyToTicketCallbackData().new(ticket_id=support_ticket.id),
                ),
                InlineKeyboardButton(
                    text='❌ Close ticket',
                    callback_data=CloseSupportTicketCallbackData().new(ticket_id=support_ticket.id),
                ),
            )
        self.insert(RemoveMessageButton())
