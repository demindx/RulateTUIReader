from typing import TYPE_CHECKING, cast
from textual import work
from textual.app import ComposeResult
from textual.containers import CenterMiddle
from textual.screen import ModalScreen
from textual.widgets import Label, ListItem, ListView

from src.models.chapter import ChapterModel

if TYPE_CHECKING:
    from src.ui.ui import UI


class ChapterListScreen(ModalScreen):
    def __init__(self, book_id: int) -> None:
        super().__init__()

        self._book_id: int = book_id
        self._scroll: ListView = ListView()
        self._modal: CenterMiddle = CenterMiddle(self._scroll)

    def compose(self) -> ComposeResult:
        yield self._modal

    async def on_mount(self) -> None:
        self._modal.border_title = "Chapters"
        self._load_chapters()

    @work()
    async def _load_chapters(self) -> None:
        service = cast("UI", self.app).service

        chapters: list[ChapterModel] = await service.book.get_chapters(self._book_id)

        for chapter in chapters:
            self._scroll.append(ListItem(Label(chapter.title)))
