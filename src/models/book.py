from pydantic import BaseModel, HttpUrl


class BookModel(BaseModel):
    id: int
    s_title: str
    t_title: str
    img: HttpUrl
    first_chapter: int | None = None
