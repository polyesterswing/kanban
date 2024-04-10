from textual.app import App, ComposeResult
from textual.widgets import Static, ListView, ListItem, Label, Header
from textual.containers import VerticalScroll, HorizontalScroll, Horizontal, Vertical
from textual.reactive import reactive

from textual.screen import Screen

class Card(Label):
    selected = reactive(False)

    def on_mouse_down(self, event) -> None:
        self.selected = not self.selected

    def watch_selected(self, selected_value):
        if selected_value:
            self.add_class("selected")
        else:
            self.remove_class("selected")

class Column(VerticalScroll):
    def __init__(self, color, cards):
        super().__init__()
        self.color = color
        self.cards = cards

    def compose(self) -> ComposeResult:
        for card in self.cards:
            yield Card(card, classes=f"card col{self.color}")

class Kanban(App):
    CSS_PATH = "main.tcss"

    def compose(self) -> ComposeResult:
        yield Label("Kanban Board", id="heading")
        with HorizontalScroll():
            with VerticalScroll():
                yield Label("Todo", classes="status")
                yield Column(1, ["abc", "def", "ghi"])
            with VerticalScroll():
                yield Label("In Progress", classes="status")
                yield Column(2, ["adjkfjdafkdj adkjsafkjfkajskdajskdjfkasjdfkjsakfjdkjfkdjskfdj", "akdjfae", "adskurakj"])
            with VerticalScroll():
                yield Label("Done", classes="status")
                yield Column(3, ["djakfjd", "akdjf"])


if __name__ == "__main__":
    app = Kanban()
    app.run()
