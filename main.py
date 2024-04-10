from textual.app import App, ComposeResult
from textual.widgets import Static, ListView, ListItem, Label, Header
from textual.containers import VerticalScroll, HorizontalScroll, Horizontal, Vertical
from textual.reactive import reactive
from textual.message import Message
from textual.css.query import NoMatches

from textual.screen import Screen

import json

class Card(Label):
    selected = reactive(False)
    text = reactive("")

    def __init__(self, text):
        super().__init__()
        self.text = text

    def watch_selected(self, selected_value):
        if selected_value:
            self.add_class("selected")
        else:
            self.remove_class("selected")

    def on_mouse_down(self, event) -> None:
        self.selected = True

    def compose(self) -> ComposeResult:
        yield Label(self.text)

class Column(VerticalScroll):
    cards = reactive([], recompose=True)

    def __init__(self, color, cards):
        super().__init__()
        self.color = color
        self.cards = cards

    def compose(self) -> ComposeResult:
        for card in self.cards:
            c = Card(card)
            c.add_class("card", f"col{self.color}")
            yield c

    def on_mouse_up(self, event) -> None:
        try:
            card = self.app.query_one(".selected")
            card.selected = False
        except NoMatches:
            pass

class Kanban(App):
    CSS_PATH = "main.tcss"

    f = open("main.json")
    data = json.load(f)

    def compose(self) -> ComposeResult:
        yield Label(self.data["heading"], id="heading")
        with HorizontalScroll():
                for col, status in enumerate(self.data["statuses"]):
                    with VerticalScroll():
                        yield Label(status["title"], classes="status")
                        yield Column(col % 3, status["cards"])

if __name__ == "__main__":
    app = Kanban()
    app.run()
