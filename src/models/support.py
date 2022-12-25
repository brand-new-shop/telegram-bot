import datetime
from typing import TypedDict

from pydantic import BaseModel

__all__ = (
    'SupportSubject',
    'SupportRequestCreate',
    'SupportRequest',
    'SupportRequestPreview',
    'SupportRequestCreated',
    'ChooseSubjectCallbackData',
    'SupportRequestDetailCallbackData',
)


class SupportSubject(BaseModel):
    id: int
    name: str


class SupportRequestCreate(BaseModel):
    user_telegram_id: int
    issue: str
    subject_id: int


class SupportRequestPreview(BaseModel):
    id: int
    issue_preview: str


class SupportRequest(BaseModel):
    id: int
    created_at: datetime.datetime
    is_open: bool
    issue: str
    answer: str | None
    subject: SupportSubject


class SupportRequestCreated(BaseModel):
    id: int


class ChooseSubjectCallbackData(TypedDict):
    support_subject_id: int


class SupportRequestDetailCallbackData(TypedDict):
    support_request_id: int
