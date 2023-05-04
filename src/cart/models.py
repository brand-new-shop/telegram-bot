from decimal import Decimal

from pydantic import BaseModel

__all__ = (
    'CartProduct',
)


class CartProduct(BaseModel):
    cart_product_id: int
    product_id: int
    product_name: str
    product_price: Decimal
    quantity: int
