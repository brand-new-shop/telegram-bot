from dataclasses import dataclass
from decimal import Decimal

__all__ = (
    'LastPurchaseDTO',
    'UserProfileDTO',
)


@dataclass(frozen=True, slots=True)
class LastPurchaseDTO:
    product_name: str
    quantity: int
    price: Decimal


@dataclass(frozen=True, slots=True)
class UserProfileDTO:
    telegram_id: int
    username: str | None
    purchases_total_count: int
    purchases_total_price: Decimal
    last_purchases: list[LastPurchaseDTO]
