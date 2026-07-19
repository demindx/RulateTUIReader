from typing import TYPE_CHECKING, cast

from textual import on, work
from textual.app import ComposeResult
from textual.containers import CenterMiddle
from textual.screen import ModalScreen
from textual.widgets import (
    Input,
    Label,
)

if TYPE_CHECKING:
    from src.ui.ui import UI


class LoginScreen(ModalScreen):
    def __init__(self) -> None:
        super().__init__()

    def compose(self) -> ComposeResult:
        self._login_input = Input(placeholder="Enter your login")
        self._pass_input = Input(placeholder="Enter your password", password=True, id="pass_input")

        with CenterMiddle():
            yield Label("Login")
            yield self._login_input

            yield Label("Password")
            yield self._pass_input

    @work()
    async def _login(self) -> None:
        service = cast("UI", self.app).service

        await service.user.login(self._login_input.value, self._pass_input.value)

    @on(Input.Submitted, "#pass_input")
    async def login(self) -> None:
        self._login()
        self.dismiss()
