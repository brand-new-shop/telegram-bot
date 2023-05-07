from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

__all__ = (
    'CoinbasePaymentCreated',
)


class CoinbasePaymentCreated(BaseModel):
    uuid: UUID
    hosted_url: str
    amount: Decimal
