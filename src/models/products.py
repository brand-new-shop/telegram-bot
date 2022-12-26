import datetime

from pydantic import BaseModel

__all__ = (
    'CategoryPreview',
    'Category',
    'ProductPreview',
    'ChooseCategoryCallbackData',
    'ChooseProductCallbackData',
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
