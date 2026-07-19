from typing import TYPE_CHECKING, cast

from textual import log, on, work
from textual.app import ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import CenterMiddle
from textual.message import Message
from textual.screen import ModalScreen
from textual.widgets import ListItem, ListView

from src.models.chapter import ChapterModel
from src.ui.widgets.chapter import Chapter as ChapterWidget

if TYPE_CHECKING:
    from src.ui.ui import UI


class ChapterListScreen(ModalScreen):
    class Selected(Message):
        def __init__(self, chapter: ChapterModel) -> None:
            super().__init__()

            self.chapter: ChapterModel = chapter

    BINDINGS: list[BindingType] = [  # type: ignore[misc]
        Binding("g", "list_top", description="scroll to top"),
        Binding("G", "list_bottom", description="scroll to bottom"),
        Binding("j", "list_down", description="scroll down"),
        Binding("k", "list_up", description="scroll up"),
    ]

    def __init__(self, book_id: int, current_chapter: ChapterModel) -> None:
        super().__init__()

        self._book_id: int = book_id
        self._scroll: ListView = ListView()
        self._chapter_modal: CenterMiddle = CenterMiddle(self._scroll)
        self._curr_chapter: ChapterModel = current_chapter

    def compose(self) -> ComposeResult:
        yield self._chapter_modal

    @on(ListView.Selected)
    async def list_view_selected(self, event: ListView.Selected) -> None:
        chapter: ChapterWidget = cast(ChapterWidget, event.item.children[0])

        self.dismiss(chapter.chapter)

    async def action_list_down(self) -> None:
        if self._scroll.index is not None:
            self._scroll.index += 1
        else:
            self._scroll.index = 0

    async def action_list_up(self) -> None:
        if self._scroll.index is not None:
            self._scroll.index -= 1
        else:
            self._scroll.index = 0

    async def action_list_top(self) -> None:
        self._scroll.index = 0

    async def action_list_bottom(self) -> None:
        self._scroll.index = len(self._scroll) - 1

    async def on_mount(self) -> None:
        log(self._curr_chapter)
        self._chapter_modal.border_title = "Chapters"
        self._load_chapters()

    @work()
    async def _load_chapters(self) -> None:
        service = cast("UI", self.app).service

        chapters: list[ChapterModel] = await service.book.get_chapters(self._book_id)

        for chapter in chapters:
            self._scroll.append(ListItem(ChapterWidget(chapter)))
