import aiohttp

from src.core.exceptions import RequestException
from src.types.bookmark import Bookmark
from src.types.chapter import Chapter
from src.types.response import RulateResponse


class BookApiClient:
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self.__session: aiohttp.ClientSession = session

    async def get_bookmarks(self) -> list[Bookmark]:
        async with self.__session.get("bookmarks") as response:
            data = RulateResponse.model_validate(await response.json())

            if data.status == "fail":
                raise RequestException(data.msg)

            bookmarks: list[Bookmark] = [
                Bookmark.model_validate(bookmark) for bookmark in data.response
            ]

            return bookmarks

    async def get_chapter(self, book_id: int, chapter_id: int) -> Chapter:
        async with self.__session.get(
            "chapter", params={"book_id": book_id, "chapter_id": chapter_id}
        ) as response:
            data = RulateResponse.model_validate(await response.json())

            if data.status == "fail":
                raise RequestException(data.msg)

            return Chapter.model_validate(data.response)

    async def get_chapters(self, book_id: int) -> list[Chapter]:
        async with self.__session.get(
            "bookChapters", params={"book_id": book_id}
        ) as response:
            data = RulateResponse.model_validate(await response.json())

            if data.status == "fail":
                raise RequestException(data.msg)

            return [Chapter.model_validate(chapter) for chapter in data.response]
