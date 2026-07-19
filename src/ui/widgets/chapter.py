from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Label

from src.models.chapter import ChapterModel


class Chapter(Widget):
    def __init__(self, chapter: ChapterModel) -> None:
        super().__init__()
        self.chapter = chapter

    def compose(self) -> ComposeResult:
        yield Label(self.chapter.title)
