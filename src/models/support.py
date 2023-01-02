import datetime
from typing import TypedDict

from pydantic import BaseModel

__all__ = (
    'SupportTicketCreate',
    'SupportRequest',
    'SupportTicketPreview',
    'SupportTicketCreated',
    'SupportRequestDetailCallbackData',
)


class SupportTicketCreate(BaseModel):
    user_telegram_id: int
    issue: str
    subject: str


class SupportTicketPreview(BaseModel):
    id: int
    subject: str
    status: str


class SupportRequest(BaseModel):
    id: int
    created_at: datetime.datetime
    is_open: bool
    issue: str
    answer: str | None
    subject: str


class SupportTicketCreated(BaseModel):
    id: int


class SupportRequestDetailCallbackData(TypedDict):
    support_request_id: int
