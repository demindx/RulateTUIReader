from typing import override

import aiohttp

from src.api.base import BaseApiClient
from src.core.interfaces.book_repo import BookRepoInterface
from src.models.book import Book
from src.models.chapter import Chapter


class BookApiClient(BookRepoInterface, BaseApiClient):
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self._session: aiohttp.ClientSession = session

    @override
    async def get_book(self, id: int) -> Book:
        params = {"book_id": id}

        async with self._session.get("book", params=params) as response:
            data = await self._validate_response(response)

            return Book.model_validate(data.response)

    @override
    async def get_chapters(self, id: int) -> list[Chapter]:
        params = {"book_id": id}

        async with self._session.get("bookChapters", params=params) as response:
            data = await self._validate_response(response)

            chapters = [Chapter.model_validate(chapter) for chapter in data.response]

            return chapters

    @override
    async def get_chapter(self, book_id: int, chapter_id: int) -> Chapter:
        params = {"book_id": book_id, "chapter_id": chapter_id}

        async with self._session.get("chapter", params=params) as response:
            data = await self._validate_response(response)

            return Chapter.model_validate(data.response)
