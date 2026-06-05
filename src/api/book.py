from typing import override

import aiohttp

from src.api.base import BaseApiClient
from src.core.interfaces.book import BookRepoInterface
from src.models.book import BookModel
from src.models.chapter import ChapterModel


class BookApiClient(BookRepoInterface, BaseApiClient):
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self._session: aiohttp.ClientSession = session

    @override
    async def get_book(self, id: int) -> BookModel:
        params = {"book_id": id}

        async with self._session.get("book", params=params) as response:
            data = await self._validate_response(response)

            return BookModel.model_validate(data.response)

    @override
    async def get_chapters(self, id: int) -> list[ChapterModel]:
        params = {"book_id": id}

        async with self._session.get("bookChapters", params=params) as response:
            data = await self._validate_response(response)

            chapters = [
                ChapterModel.model_validate(chapter) for chapter in data.response
            ]

            return chapters

    @override
    async def get_chapter(self, book_id: int, chapter_id: int) -> ChapterModel:
        params = {"book_id": book_id, "chapter_id": chapter_id}

        async with self._session.get("chapter", params=params) as response:
            data = await self._validate_response(response)

            return ChapterModel.model_validate(data.response)
