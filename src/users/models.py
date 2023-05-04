import datetime
from dataclasses import dataclass
from decimal import Decimal

from pydantic import BaseModel

from products.models import OrderPreview


@dataclass(frozen=True, slots=True)
class UserProfileDTO:
    telegram_id: int
    username: str | None
    purchases_total_count: int
    purchases_total_price: Decimal
    last_purchases: list[OrderPreview]


class User(BaseModel):
    created_at: datetime.datetime
    telegram_id: int
    username: str | None
    balance: Decimal
    is_banned: bool
