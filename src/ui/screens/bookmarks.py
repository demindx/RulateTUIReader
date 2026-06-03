from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header

from src.services.app import AppService


class BookmarksScreen(Screen):
    def __init__(self, service: AppService) -> None:
        super().__init__()

        self._servcie: AppService = service

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
