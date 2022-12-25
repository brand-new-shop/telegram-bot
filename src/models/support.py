from pydantic import BaseModel

__all__ = (
    'SupportSubject',
)


class SupportSubject(BaseModel):
    id: int
    name: str
