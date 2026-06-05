from textual import on
from textual.app import ComposeResult
from textual.containers import CenterMiddle
from textual.screen import ModalScreen
from textual.widgets import (
    Input,
    Label,
)

from src.services.app import AppService


class LoginScreen(ModalScreen):
    DEFAULT_CSS = """
    LoginScreen {
        align: center middle;
        background: $background 60%;
    }

    LoginScreen > CenterMiddle {
        width: 50%;
        height: auto;
        background: $panel;
        border: thick $primary;
        padding: 2 4;
    }
    """

    def __init__(self, service: AppService) -> None:
        super().__init__()
        self._service: AppService = service

    def compose(self) -> ComposeResult:
        self._login_input = Input(placeholder="Enter your login")
        self._pass_input = Input(
            placeholder="Enter your password", password=True, id="pass_input"
        )

        with CenterMiddle():
            yield Label("Login")
            yield self._login_input

            yield Label("Password")
            yield self._pass_input

    @on(Input.Submitted, "#pass_input")
    async def login(self) -> None:
        await self._service.user.login(self._login_input.value, self._pass_input.value)
        self.dismiss()
