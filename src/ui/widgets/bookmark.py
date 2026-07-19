from typing import TYPE_CHECKING, cast

from textual import work
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Label, LoadingIndicator
from textual_image.widget import Image

from src.core.exceptions import RequestError
from src.models.bookmark import BookmarkModel
from src.models.chapter import ChapterModel
from src.services.app import AppService

if TYPE_CHECKING:
    from src.ui.ui import UI


class Bookmark(Widget):
    class Selected(Message):
        def __init__(self, bookmark: BookmarkModel) -> None:
            super().__init__()
            self.bookmark = bookmark

    def __init__(self, bookmark: BookmarkModel) -> None:
        self.image = Image(classes="bookmark-cover")
        self.bookmark: BookmarkModel = bookmark
        self.chapter: ChapterModel | None = None

        self._title_label: Label = Label(self.bookmark.book.t_title, classes="bookmark-title")
        self._subtitle_label: Label = Label(self.bookmark.book.t_title, classes="bookmark-subtitle")

        self._last_readed_label: Label = Label(
            classes="bookmark-meta",
        )

        self._new_chapters_label: Label = Label(
            (
                f"Новых глав: {self.bookmark.new_chapters} "
                f"({self.bookmark.free_new_chapters} бесплатных)"
            ),
            classes="bookmark-meta",
        )

        super().__init__()

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield self.image
            yield LoadingIndicator(id="cover-loader")
            with Vertical(classes="bookmark-content"):
                yield self._title_label
                yield self._subtitle_label
                yield self._last_readed_label
                yield self._new_chapters_label

    @property
    def service(self) -> AppService:
        return cast("UI", self.app).service

    @work()
    async def _load_image(self) -> None:
        image = await self.service.image.get_image(self.bookmark.book.img, (160, 220))

        self.image.image = image
        self.query_one("#cover-loader", LoadingIndicator).display = False
        self.image.display = True

    @work()
    async def _load_chapter(self) -> None:
        if self.bookmark.last_readed == 0:
            self._last_readed_label.update("Последняя открытая глава: Не была открыта")
            return

        try:
            self.chapter = await self.service.book.get_chapter(
                self.bookmark.book.id, self.bookmark.last_readed
            )
            self._last_readed_label.update(f"Последняя открытая глава: {self.chapter.title}")
        except RequestError as e:
            self._last_readed_label.update(f"Последняя открытая глава: {e}")

    def on_mount(self) -> None:
        self._load_image()
        self._load_chapter()

    async def on_click(self) -> None:
        self.post_message(self.Selected(self.bookmark))
