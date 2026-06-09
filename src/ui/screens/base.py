from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header
from textual.containers import Container


class BaseScreen(Screen):
    def __init__(self) -> None:
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()

        with Container(classes="main_wrapper"):
            yield from self.compose_result()

        yield Footer()

    def compose_result(self) -> ComposeResult:
        yield from []
