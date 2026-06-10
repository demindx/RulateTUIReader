from typing import cast, TYPE_CHECKING
from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding, BindingType
from textual.widgets import ListItem, ListView

from src.ui.screens.base import BaseScreen
from src.ui.screens.chapter import ChapterScreen
from src.ui.widgets.bookmark import Bookmark

if TYPE_CHECKING:
    from src.ui.ui import UI


class BookmarksScreen(BaseScreen):
    BINDINGS: list[BindingType] = [
        Binding("g", "list_top"),
        Binding("G", "list_bottom"),
        Binding("j", "list_down"),
        Binding("k", "list_up"),
    ]

    def __init__(self) -> None:
        super().__init__()

        self._avatar_worker = None
        self._service = cast("UI", self.app).service

        self._bookmarks_contaner = ListView()

    def compose_result(self) -> ComposeResult:
        yield self._bookmarks_contaner

    @work()
    async def _load_bookmark(self) -> None:
        bookmarks = await self._service.user.get_bookmarks()

        for bookmark in bookmarks:
            item = ListItem(Bookmark(bookmark))
            self._bookmarks_contaner.append(item)

    async def action_list_down(self) -> None:
        if self._bookmarks_contaner.index is not None:
            self._bookmarks_contaner.index += 1
        else:
            self._bookmarks_contaner.index = 0

    async def action_list_up(self) -> None:
        if self._bookmarks_contaner.index is not None:
            self._bookmarks_contaner.index -= 1
        else:
            self._bookmarks_contaner.index = 0

    async def action_list_top(self) -> None:
        self._bookmarks_contaner.index = 0

    async def action_list_bottom(self) -> None:
        self._bookmarks_contaner.index = len(self._bookmarks_contaner) - 1

    @on(ListView.Selected)
    async def list_view_selected(self, event: ListView.Selected) -> None:
        bookmark: Bookmark = cast(Bookmark, event.item.children[0])

        self.post_message(Bookmark.Selected(bookmark.bookmark))

    def on_mount(self) -> None:
        self._load_bookmark()

    @on(Bookmark.Selected)
    async def open_chapter(self, event: Bookmark.Selected) -> None:
        bookmark = event.bookmark
        chapter_id = bookmark.last_readed

        if chapter_id == 0:
            book = await self._service.book.get_book(bookmark.book.id)
            chapter_id = book.first_chapter

        if chapter_id is None:
            raise ValueError("chapter_id cannot be None.")

        app = cast("UI", self.app)
        app.push_screen(ChapterScreen(book_id=bookmark.book.id, chapter_id=chapter_id))
