from pydantic import BaseModel


class Chapter(BaseModel):
    id: int
    title: str
    ord: int | None = None
    text: str | None = None
    next_chap: int | None = None
    prev_chap: int | None = None
    subscription_price: int | None = None
