from pydantic import BaseModel, HttpUrl


class UserModel(BaseModel):
    id: int
    login: str
    token: str | None = None
    avatar: HttpUrl
    balance: float
