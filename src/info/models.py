from pydantic import BaseModel

__all__ = ('ShopInfo',)


class ShopInfo(BaseModel):
    key: str
    value: str
