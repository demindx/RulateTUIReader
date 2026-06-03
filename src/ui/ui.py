from textual import on
from textual.app import App

from src.services.app import AppService
from src.ui.screens.bookmarks import BookmarksScreen
from src.ui.screens.login import LoginScreen


class UI(App):
    TITLE = "tuiReader"

    def __init__(self, service: AppService) -> None:
        super().__init__()
        self._service: AppService = service

    async def on_mount(self) -> None:
        self._service.keyring.delete_token()
        self.push_screen(BookmarksScreen(self._service))

        if not self._service.keyring.get_token():
            self.push_screen(LoginScreen(self._service))

    @on(LoginScreen.UserLoggedIn)
    async def remove_login_screen(self) -> None:
        self.pop_screen()
