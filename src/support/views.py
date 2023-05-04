from collections.abc import Iterable

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from core.views import View
from info.models import ShopInfo
from support import models
from support.callback_data import (
    ReplyToTicketDetailCallbackData,
    CreateReplyToTicketCallbackData,
    CloseSupportTicketCallbackData,
    SupportTicketDetailCallbackData,
)
from users.keyboards import RemoveMessageButton

__all__ = (
    'SupportTicketCreatedView',
    'SupportTicketDetailView',
    'SupportTicketsListView',
    'AcceptSupportRulesView',
    'ReplyToTicketDetailView',
)


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


class AcceptSupportRulesView(View):

    def __init__(self, support_rules: ShopInfo):
        self.__support_rules = support_rules

    def get_text(self) -> str:
        return self.__support_rules.value

    def get_reply_markup(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[[KeyboardButton('✅ I did')]],
        )


class SupportTicketCreatedView(View):
    reply_markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[[KeyboardButton('⬅️ Back')]],
    )

    def __init__(self, ticket_id: int):
        self.__ticket_id = ticket_id

    def get_text(self) -> str:
        return (
            'Your Support Enquiry has been sent.'
            ' We will respond within the next few hours.'
            ' Please expect delays on holidays and weekends.'
            f'\nRequest number: #{self.__ticket_id}'
        )


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
        markup = InlineKeyboardMarkup(row_width=1)
        for i, reply_id in enumerate(self.__reply_ids, start=1):
            markup.insert(InlineKeyboardButton(
                text=f'Reply #{i}',
                callback_data=ReplyToTicketDetailCallbackData().new(
                    ticket_reply_id=reply_id),
            ))

        if self.__ticket.status != 'Closed':
            markup.row(
                InlineKeyboardButton(
                    text='➕ Reply',
                    callback_data=CreateReplyToTicketCallbackData().new(
                        ticket_id=self.__ticket.id),
                ),
                InlineKeyboardButton(
                    text='❌ Close ticket',
                    callback_data=CloseSupportTicketCallbackData().new(
                        ticket_id=self.__ticket.id),
                ),
            )
        markup.insert(RemoveMessageButton())
        return markup


class SupportTicketsListView(View):
    text = '📚 My Support Requests'

    def __init__(self, tickets: Iterable[models.SupportTicketPreview]):
        self.__tickets = tickets

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            *(
                InlineKeyboardButton(
                    text=f'{ticket.status} - #{ticket.id} - {ticket.subject}',
                    callback_data=SupportTicketDetailCallbackData().new(
                        ticket_id=ticket.id),
                )
                for ticket in self.__tickets
            ),
            RemoveMessageButton(),
        )
        return markup
