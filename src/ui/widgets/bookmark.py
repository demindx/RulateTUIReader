from textual import work
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Label
from textual_image.widget import Image

from src.models.bookmark import BookmarkModel


class Bookmark(Widget):
    def __init__(self, bookmark: BookmarkModel) -> None:
        self.image = Image()
        self.bookmark: BookmarkModel = bookmark

        self._title_label: Label = Label(self.bookmark.book.s_title)

        super().__init__()

    def compose(self) -> ComposeResult: ...
