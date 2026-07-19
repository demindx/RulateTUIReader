from typing import TYPE_CHECKING, cast

from markdownify import markdownify as md
from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Button, Label, Markdown

from src.models.chapter import ChapterModel
from src.services.app import AppService
from src.ui.screens.base import BaseScreen
from src.ui.screens.modals.chapter_list import ChapterListScreen

if TYPE_CHECKING:
    from src.ui.ui import UI


class ChapterScreen(BaseScreen):
    BINDINGS: list[BindingType] = [  # type: ignore[misc]
        Binding("j", "scroll_down", description="scroll down"),
        Binding("k", "scroll_up", description="scroll up"),
        Binding("g", "scroll_top", description="scroll to top"),
        Binding("G", "scroll_bottom", description="scroll to bottom"),
        Binding("h", "prev_chap", description="open previous chapter"),
        Binding("l", "next_chap", description="open next chapter"),
        Binding("q", "close_chapter", description="close current chapter"),
        Binding("o", "open_chapters_list", description="open chapters list"),
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

    def action_scroll_top(self) -> None:
        self._scroll.action_scroll_home()

    def action_scroll_bottom(self) -> None:
        self._scroll.action_scroll_end()

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

    def action_close_chapter(self) -> None:
        self.dismiss()

    def action_open_chapters_list(self) -> None:
        app = cast("UI", self.app)

        if self._chapter:
            app.push_screen(
                screen=ChapterListScreen(self._book_id, self._chapter),
                callback=self._chapter_selected,
            )

    @on(Button.Pressed, "#next_chap")
    async def next_chap(self) -> None:
        self.action_next_chap()

    @on(Button.Pressed, "#prev_chap")
    async def prev_chap(self) -> None:
        self.action_prev_chap()

    async def _chapter_selected(self, chapter: ChapterModel | None) -> None:
        if chapter:
            self._chapter_id = chapter.id
            self._load_chapter()

    async def on_mount(self) -> None:
        self._load_chapter()
