import datetime
from decimal import Decimal

from pydantic import BaseModel
from typing_extensions import TypedDict

__all__ = (
    'CategoryPreview',
    'Category',
    'ProductPreview',
    'ChooseCategoryCallbackData',
    'ChooseProductCallbackData',
    'OrdersTotalCount',
    'OrderPreview',
    'OrdersStatistics',
    'Product',
)


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


class AddToCartCallbackData(TypedDict):
    product_id: int


class OrderPreview(BaseModel):
    id: int
    product_name: str
    quantity: int
    total_price: Decimal


class OrdersTotalCount(BaseModel):
    user_telegram_id: int
    orders_total_count: int


class OrdersStatistics(BaseModel):
    user_telegram_id: int
    orders_count: int
    orders_total_price: Decimal


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: Decimal
    stocks_count: int
    min_order_quantity: int
    max_order_quantity: int
    max_replacement_time_in_minutes: int
    are_stocks_displayed: bool
    is_hidden: bool
    can_be_purchased: bool
    category: Category
    picture_urls: tuple[str, ...]
