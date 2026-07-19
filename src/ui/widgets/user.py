from typing import TYPE_CHECKING, cast

from textual import work
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label
from textual_image.widget import Image

if TYPE_CHECKING:
    from src.ui.ui import UI


class User(Widget):
    balance = reactive(0.0)

    def __init__(self) -> None:
        self._avatar = Image()
        self._balance_label: Label = Label("0")
        super().__init__()

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield self._balance_label
            yield self._avatar

    def watch_balance(self, balance: float) -> None:
        self._balance_label.update(str(balance))

    @work()
    async def _load_user(self) -> None:
        service = cast("UI", self.app).service

        user = await service.user.get_me()
        self.balance = user.balance
        self._avatar.image = await service.image.get_rounded_image(
            user.avatar, (100, 100)
        )

    def on_mount(self) -> None:
        self._load_user()
