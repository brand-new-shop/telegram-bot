import datetime
from decimal import Decimal

from pydantic import BaseModel

__all__ = (
    'CategoryPreview',
    'Category',
    'ProductPreview',
    'ChooseCategoryCallbackData',
    'ChooseProductCallbackData',
    'OrderPreview',
    'OrdersStatistics',
)

from typing_extensions import TypedDict


class CategoryPreview(BaseModel):
    id: int
    name: str
    emoji_icon: str | None


class Category(BaseModel):
    id: int
    name: str
    emoji_icon: str | None
    parent: int
    is_hidden: bool
    created_at: datetime.datetime


class ProductPreview(BaseModel):
    id: int
    name: str


class ChooseCategoryCallbackData(TypedDict):
    category_id: int


class ChooseProductCallbackData(TypedDict):
    product_id: int


class OrderPreview(BaseModel):
    id: int
    product_name: str
    quantity: int
    total_price: Decimal


class OrdersStatistics(BaseModel):
    user_telegram_id: int
    orders_count: int
    orders_total_price: Decimal
