from markdownify import markdownify as md
from typing import TYPE_CHECKING, cast
from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Button, Label, Markdown

from src.models.chapter import ChapterModel
from src.services.app import AppService
from src.ui.screens.base import BaseScreen


if TYPE_CHECKING:
    from src.ui.ui import UI


class ChapterScreen(BaseScreen):
    BINDINGS: list[BindingType] = [
        Binding("j", "scroll_down"),
        Binding("k", "scroll_up"),
    ]

    def __init__(self, chapter_id: int, book_id: int) -> None:
        super().__init__()
        self._chapter_id: int = chapter_id
        self._book_id: int = book_id

        self._chapter_text = Markdown()
        self._label = Label()

        self._scroll = VerticalScroll()

        self._next_chap_btn = Button("Next chapter", id="next_chap")
        self._prev_chap_btn = Button("Previous chapter", id="prev_chap")

        self._chapter: ChapterModel | None = None

    def compose_result(self) -> ComposeResult:
        yield self._label
        with self._scroll:
            yield self._chapter_text

            with Horizontal():
                yield self._prev_chap_btn
                yield self._next_chap_btn

    @work()
    async def _load_chapter(self) -> None:
        service: AppService = cast("UI", self.app).service

        self._chapter = await service.book.get_chapter(
            book_id=self._book_id, chapter_id=self._chapter_id
        )

        if self._chapter.text:
            self._chapter_text.update(md(self._chapter.text))

        self._label.update(f"[bold]{self._chapter.title}[/bold]")

    def action_scroll_down(self) -> None:
        self._scroll.action_scroll_down()

    def action_scroll_up(self) -> None:
        self._scroll.action_scroll_up()

    def action_next_chap(self) -> None:
        if self._chapter and self._chapter.next_chap:
            self._chapter_id = self._chapter.next_chap

            self._load_chapter()

            self._scroll.action_scroll_home()

    def action_prev_chap(self) -> None:
        if self._chapter and self._chapter.prev_chap:
            self._chapter_id = self._chapter.prev_chap

            self._load_chapter()

            self._scroll.action_scroll_home()

    @on(Button.Pressed, "#next_chap")
    async def next_chap(self) -> None:
        self.action_next_chap()

    @on(Button.Pressed, "#prev_chap")
    async def prev_chap(self) -> None:
        self.action_prev_chap()

    async def on_mount(self) -> None:
        self._load_chapter()
