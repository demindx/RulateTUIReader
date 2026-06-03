from enum import Enum
from typing import Self
from pydantic import BaseModel

from src.types.book import Book


class BookmarkType(Enum):
    READ = (0, "Читаю")
    FAUVORITES = (1, "Избранные")
    IN_PLAN = (2, "В планах")
    THROWED = (3, "Заброшено")
    READED = (4, "Прочитано")

    def __new__(cls, int_val: int, label: str) -> Self:
        obj = object.__new__(cls)
        obj._value_ = int_val

        return obj

    def __init__(self, int_val: int, label: str) -> None:
        self.label = label

    def __str__(self) -> str:
        return self.label


class Bookmark(BaseModel):
    last_readed: int
    new_chapters: int
    free_new_chapters: int
    type: BookmarkType
    book: Book
