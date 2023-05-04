from decimal import Decimal
from typing import TypedDict

from pydantic import BaseModel, Field

__all__ = (
    'CartProduct',
    'ChangeProductQuantityInCartTypedDict',
    'HasProductQuantityTypedDict',
    'HasCartProductIdTypedDict',
    'HasProductIdTypedDict',
)


class HasCartProductIdTypedDict(TypedDict):
    cart_product_id: int


class HasProductQuantityTypedDict(TypedDict):
    quantity: int


class HasProductIdTypedDict(TypedDict):
    product_id: int


class ChangeProductQuantityInCartTypedDict(
    HasCartProductIdTypedDict,
    HasProductQuantityTypedDict,
    HasProductIdTypedDict,
):
    pass


class CartProduct(BaseModel):
    id: int = Field(alias='cart_product_id')
    product_id: int
    product_name: str
    product_price: Decimal
    quantity: int
