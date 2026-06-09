from typing import cast, TYPE_CHECKING
from textual import work
from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll

from src.ui.screens.base import BaseScreen
from src.ui.widgets.bookmark import Bookmark
from src.ui.widgets.user import User as UserWidget

if TYPE_CHECKING:
    from src.ui.ui import UI


class BookmarksScreen(BaseScreen):
    def __init__(self) -> None:
        super().__init__()

        self._user_widget: UserWidget = UserWidget()
        self._avatar_worker = None
        self._service = cast("UI", self.app).service

        self._bookmarks_contaner = VerticalScroll()

    def compose_result(self) -> ComposeResult:
        with Vertical(classes="wrapper"):
            yield self._bookmarks_contaner
            yield self._user_widget

    @work()
    async def _load_bookmark(self) -> None:
        bookmarks = await self._service.user.get_bookmarks()

        for bookmark in bookmarks:
            self._bookmarks_contaner.mount(Bookmark(bookmark))

    def on_mount(self) -> None:
        self._load_bookmark()
