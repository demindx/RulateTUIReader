from src.core.interfaces.book import BookRepoInterface
from src.models.book import BookModel
from src.models.chapter import ChapterModel


class BookService:
    def __init__(self, repo: BookRepoInterface) -> None:
        self._repo: BookRepoInterface = repo

    async def get_book(self, id: int) -> BookModel:
        return await self._repo.get_book(id)

    async def get_chapters(self, book_id: int) -> list[ChapterModel]:
        return await self._repo.get_chapters(book_id)

    async def get_chapter(self, book_id: int, chapter_id: int) -> ChapterModel:
        return await self._repo.get_chapter(book_id, chapter_id)
