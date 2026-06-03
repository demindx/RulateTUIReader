from pydantic import BaseModel, HttpUrl


class Book(BaseModel):
    id: int
    s_title: str
    t_title: str
    img: HttpUrl
    first_chapter: int | None = None
