from pydantic import BaseModel, HttpUrl


class User(BaseModel):
    id: int
    login: str
    token: str | None = None
    avatar: HttpUrl
    balance: float
