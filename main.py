from textual.app import App, ComposeResult
from textual.widgets import Static, ListView, ListItem, Label, Header
from textual.containers import VerticalScroll, HorizontalScroll, Horizontal, Vertical
from textual.reactive import reactive
from textual.message import Message
from textual.css.query import NoMatches

from textual.screen import Screen

import json

from dataclasses import dataclass

@dataclass(frozen=True)
class CardData():
    id: int
    text: str

class Card(Label):
    selected = reactive(False)
    card = reactive(CardData(0, ""))

    def __init__(self, card):
        super().__init__()
        self.card = card

    def watch_selected(self, selected_value):
        if selected_value:
            self.add_class("selected")
        else:
            self.remove_class("selected")

    def on_mouse_down(self, event) -> None:
        self.selected = True

    def compose(self) -> ComposeResult:
        yield Label(self.card.text)

class Column(VerticalScroll):
    cards = reactive([], recompose=True)

    class CardMoved(Message):
        def __init__(self, fro, to):
            self.fro = fro
            self.to = to
            super().__init__()

    def __init__(self, color, cards):
        super().__init__()
        self.color = color
        self.cards = cards

    def compose(self) -> ComposeResult:
        for card in self.cards:
            c = Card(card)
            c.add_class("card", f"col{self.color % 3}")
            yield c

    def on_mouse_up(self, event) -> None:
        try:
            card = self.app.query_one(".selected")
            card.selected = False
            self.post_message(self.CardMoved(card.card, self.color))
        except NoMatches:
            pass

def process_data(data):
    counter = 0
    for status in data["statuses"]:
        new_cards = []
        for card in status["cards"]:
            new_cards.append(CardData(counter, card))
            counter += 1

        status["cards"] = new_cards

class Kanban(App):
    CSS_PATH = "main.tcss"

    f = open("main.json")
    data = json.load(f)

    process_data(data)

    def on_column_card_moved(self, message):
        for status in self.data["statuses"]:
            for idx, card in enumerate(status["cards"]):
                if card.id == message.fro.id:
                    status["cards"].pop(idx)
                    break

        self.data["statuses"][message.to]["cards"].append(message.fro)

        self.refresh(layout=True, recompose=True)


    def compose(self) -> ComposeResult:
        yield Label(self.data["heading"], id="heading")
        with HorizontalScroll():
                for col, status in enumerate(self.data["statuses"]):
                    with VerticalScroll():
                        yield Label(status["title"], classes="status")
                        yield Column(col, status["cards"])

if __name__ == "__main__":
    app = Kanban()
    app.run()
