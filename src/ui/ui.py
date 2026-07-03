from textual.app import App

from src.services.app import AppService

from src.ui.screens.bookmarks import BookmarksScreen
from src.ui.screens.modals.login import LoginScreen


class UI(App):
    TITLE = "RulateTUIReader"
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
