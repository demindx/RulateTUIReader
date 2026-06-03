from src.core.interfaces.book_repo import BookRepoInterface
from src.models.book import Book
from src.models.chapter import Chapter


class BookService:
    def __init__(self, repo: BookRepoInterface) -> None:
        self._repo: BookRepoInterface = repo

    async def get_book(self, id: int) -> Book:
        return await self._repo.get_book(id)

    async def get_chapters(self, book_id: int) -> list[Chapter]:
        return await self._repo.get_chapters(book_id)

    async def get_chapter(self, book_id: int, chapter_id: int) -> Chapter:
        return await self._repo.get_chapter(book_id, chapter_id)
