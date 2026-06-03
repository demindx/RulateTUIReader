from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Markdown, TabPane, TabbedContent

from src.ui.screens.login import LoginScreen


class UI(App):
    TITLE = "tuiReader"

    async def on_mount(self) -> None:
        self.install_screen(LoginScreen(), "login")
        self.push_screen("login")
