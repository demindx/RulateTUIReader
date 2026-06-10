from textual.app import App
from textual import on

from src.services.app import AppService

from src.ui.screens.bookmarks import BookmarksScreen
from src.ui.screens.chapter import ChapterScreen
from src.ui.screens.login import LoginScreen
from src.ui.widgets.bookmark import Bookmark


class UI(App):
    TITLE = "tuiReader"
    CSS_PATH = "style.tcss"

    def __init__(self, service: AppService) -> None:
        super().__init__()
        self._service: AppService = service

    @property
    def service(self) -> AppService:
        return self._service

    async def on_mount(self) -> None:
        self.push_screen(BookmarksScreen())

        if not self._service.keyring.get_token():
            self.push_screen(LoginScreen())

    @on(Bookmark.Selected)
    async def open_chapter(self, event: Bookmark.Selected) -> None:
        bookmark = event.bookmark
        chapter_id = bookmark.last_readed

        if chapter_id == 0:
            book = await self._service.book.get_book(bookmark.book.id)
            chapter_id = book.first_chapter

        if chapter_id is None:
            raise ValueError("chapter_id cannot be None.")

        self.push_screen(ChapterScreen(book_id=bookmark.book.id, chapter_id=chapter_id))
