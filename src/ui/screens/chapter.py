from markdownify import markdownify as md
from typing import TYPE_CHECKING, cast
from textual import work
from textual.app import ComposeResult
from textual.widgets import Markdown

from src.models.chapter import ChapterModel
from src.services.app import AppService
from src.ui.screens.base import BaseScreen


if TYPE_CHECKING:
    from src.ui.ui import UI


class ChapterScreen(BaseScreen):
    def __init__(self, chapter_id: int, book_id: int) -> None:
        super().__init__()
        self._chapter_id: int = chapter_id
        self._book_id: int = book_id
        self._chapter_text = Markdown()

    def compose_result(self) -> ComposeResult:
        yield self._chapter_text

    @work()
    async def _load_chapter(self) -> None:
        service: AppService = cast("UI", self.app).service

        chapter: ChapterModel = await service.book.get_chapter(
            book_id=self._book_id, chapter_id=self._chapter_id
        )

        if chapter.text:
            self._chapter_text.append(md(chapter.text))

    async def on_mount(self) -> None:
        self._load_chapter()
