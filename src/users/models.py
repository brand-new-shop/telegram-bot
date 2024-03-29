import datetime
from decimal import Decimal

from pydantic import BaseModel


class User(BaseModel):
    created_at: datetime.datetime
    telegram_id: int
    username: str | None
    balance: Decimal
    is_banned: bool
