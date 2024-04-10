from textual.app import App, ComposeResult
from textual.widgets import Static, ListView, ListItem, Label, Header
from textual.containers import VerticalScroll, HorizontalScroll, Horizontal, Vertical

from textual.screen import Screen

class Column(VerticalScroll):
    def __init__(self, color):
        super().__init__()
        self.color = color

    def compose(self) -> ComposeResult:
        for i in range(3):
            yield Label("abc", classes=f"card col{self.color}")

class Kanban(App):
    CSS_PATH = "main.tcss"

    def compose(self) -> ComposeResult:
        yield Label("Kanban Board", id="heading")
        with HorizontalScroll():
            with VerticalScroll():
                yield Label("Todo", classes="status")
                yield Column(1)
            with VerticalScroll():
                yield Label("In Progress", classes="status")
                yield Column(2)
            with VerticalScroll():
                yield Label("Done", classes="status")
                yield Column(3)


if __name__ == "__main__":
    app = Kanban()
    app.run()
