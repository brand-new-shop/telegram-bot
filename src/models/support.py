import datetime
from typing import TypedDict

from pydantic import BaseModel

__all__ = (
    'SupportTicketCreate',
    'SupportTicket',
    'SupportTicketPreview',
    'SupportTicketCreated',
    'SupportTicketDetailCallbackData',
    'CloseSupportTicketCallbackData',
    'ReplyToTicketDetailCallbackData',
    'ReplyToTicketCreateCallbackData',
    'ReplyToTicketCreated',
    'ReplyToTicket',
)


class SupportTicketCreate(BaseModel):
    user_telegram_id: int
    issue: str
    subject: str


class SupportTicketPreview(BaseModel):
    id: int
    subject: str
    status: str


class SupportTicket(BaseModel):
    id: int
    created_at: datetime.datetime
    issue: str
    answer: str | None
    subject: str
    status: str


class SupportTicketCreated(BaseModel):
    id: int


class SupportTicketDetailCallbackData(TypedDict):
    ticket_id: int


class CloseSupportTicketCallbackData(TypedDict):
    ticket_id: int


class ReplyToTicketCreateCallbackData(TypedDict):
    ticket_id: int


class ReplyToTicketDetailCallbackData(TypedDict):
    ticket_reply_id: int


class ReplyToTicketCreated(BaseModel):
    id: int


class ReplyToTicket(BaseModel):
    id: int
    created_at: datetime.datetime
    issue: str
    answer: str | None
    ticket: SupportTicket
