from typing import cast, TYPE_CHECKING
from textual import work
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Label
from textual_image.widget import Image

from src.models.bookmark import BookmarkModel

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

        self._title_label: Label = Label(
            self.bookmark.book.t_title, classes="bookmark-title"
        )
        self._subtitle_label: Label = Label(
            self.bookmark.book.t_title, classes="bookmark-subtitle"
        )
        self._last_readed_label: Label = Label(
            f"Последняя глава: {self.bookmark.last_readed}",
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
            with Vertical(classes="bookmark-content"):
                yield self._title_label
                yield self._subtitle_label
                yield self._last_readed_label
                yield self._new_chapters_label

    @work()
    async def _load_image(self) -> None:
        service = cast("UI", self.app).service

        image = await service.image.get_image(self.bookmark.book.img, (160, 220))

        self.image.image = image

    def on_mount(self) -> None:
        self._load_image()

    async def on_click(self) -> None:
        self.post_message(self.Selected(self.bookmark))
