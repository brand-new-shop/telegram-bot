from decimal import Decimal
from typing import TypedDict

from pydantic import BaseModel

__all__ = (
    'CartProduct',
    'HasProductIdAndQuantityTypedDict',
    'HasProductQuantityTypedDict',
    'HasProductIdTypedDict',
)


class HasProductIdTypedDict(TypedDict):
    product_id: int


class HasProductQuantityTypedDict(TypedDict):
    quantity: int


class HasProductIdAndQuantityTypedDict(
    HasProductIdTypedDict,
    HasProductQuantityTypedDict,
):
    pass


class CartProduct(BaseModel):
    cart_product_id: int
    product_id: int
    product_name: str
    product_price: Decimal
    quantity: int
