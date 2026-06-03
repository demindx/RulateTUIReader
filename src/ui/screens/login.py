from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import (
    Footer,
    Header,
    Input,
    Label,
)


class LoginScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Login")
        yield Input()
        yield Label("Password")
        yield Input()
        yield Footer()
