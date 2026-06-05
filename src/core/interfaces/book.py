from abc import ABC, abstractmethod

from src.models.book import BookModel
from src.models.chapter import ChapterModel


class BookRepoInterface(ABC):
    @abstractmethod
    async def get_book(self, id: int) -> BookModel: ...

    @abstractmethod
    async def get_chapters(self, id: int) -> list[ChapterModel]: ...

    @abstractmethod
    async def get_chapter(self, book_id: int, chapter_id: int) -> ChapterModel: ...
