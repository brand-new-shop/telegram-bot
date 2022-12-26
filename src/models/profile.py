from dataclasses import dataclass
from decimal import Decimal

from models.products import OrderPreview

__all__ = (
    'UserProfileDTO',
)


@dataclass(frozen=True, slots=True)
class UserProfileDTO:
    telegram_id: int
    username: str | None
    purchases_total_count: int
    purchases_total_price: Decimal
    last_purchases: list[OrderPreview]
