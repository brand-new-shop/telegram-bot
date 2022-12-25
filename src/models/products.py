from pydantic import BaseModel

__all__ = ('Category',)


class Category(BaseModel):
    id: int
    name: str
    emoji_icon: str | None
