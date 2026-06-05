from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label
from textual_image.widget import Image


class User(Widget):
    DEFAULT_CSS = """
    User {
        dock: bottom;
        width: 100%;
        height: auto;
        margin-bottom: 1;
        padding: 1 2;
        content-align: center middle;
    }

    User > Horizontal {
        width: 100%;
        height: auto;
        align: center middle;
    }

    User Label {
        margin-right: 1;
        height: 3;
        content-align: center middle;
        text-style: bold;
    }

    User Image {
        width: 6;
        height: 3;
    }
    """

    balance = reactive(0.0)

    def __init__(self) -> None:
        self.avatar = Image()
        self._balance_label: Label = Label("0")
        super().__init__()

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield self._balance_label
            yield self.avatar

    def watch_balance(self, balance: float) -> None:
        self._balance_label.update(str(balance))
