from textual import work
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header

from src.services.app import AppService
from src.ui.widgets.user import User as UserWidget


class BookmarksScreen(Screen):
    def __init__(self, service: AppService) -> None:
        super().__init__()

        self._servcie: AppService = service
        self._user_widget: UserWidget = UserWidget()
        self._avatar_worker = None

    def compose(self) -> ComposeResult:
        yield Header()

        yield self._user_widget
        yield Footer()

    @work()
    async def _load_avatar(self) -> None:
        user = await self._servcie.user.get_me()
        img = await self._servcie.image.get_rounded_image(user.avatar)

        self._user_widget.balance = user.balance
        self._user_widget.avatar.image = img

    async def on_mount(self) -> None:
        if self._servcie.keyring.get_token():
            self._avatar_worker = self._load_avatar()

    async def on_unmount(self) -> None:
        if self._avatar_worker:
            self._avatar_worker.cancel()
