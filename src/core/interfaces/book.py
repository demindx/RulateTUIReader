from abc import ABC, abstractmethod

from src.models.book import Book
from src.models.chapter import Chapter


class BookRepoInterface(ABC):
    @abstractmethod
    async def get_book(self, id: int) -> Book: ...

    @abstractmethod
    async def get_chapters(self, id: int) -> list[Chapter]: ...

    @abstractmethod
    async def get_chapter(self, book_id: int, chapter_id: int) -> Chapter: ...
