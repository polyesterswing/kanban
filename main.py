from textual.app import App, ComposeResult
from textual.widgets import Static, ListView, ListItem, Label, Header, Footer, Input
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

    def on_mount(self) -> None:
        self.border_title = str(self.card.id)

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

    return counter

def delete_card_by_id(data, id):
    for status in data["statuses"]:
        for idx, card in enumerate(status["cards"]):
            if card.id == id:
                status["cards"].pop(idx)

def add_card_by_col_id(data, id, text, new_id):
    for idx, status in enumerate(data["statuses"]):
        if idx == id:
            status["cards"].append(CardData(new_id, text))

def modify_card_by_id(data, id, text):
    for status in data["statuses"]:
        for idx, card in enumerate(status["cards"]):
            if card.id == id:

                card_data = CardData(card.id, text)
                status["cards"][idx] = card_data

def add_status(data, name):
    data["statuses"].append({"title": name, "cards": []})

def swap_status(data, fro, to):
    statuses = data["statuses"]
    to_status = statuses[int(to)].copy()
    fro_status = statuses[int(fro)].copy()

    data["statuses"][int(fro)] = to_status
    data["statuses"][int(to)] = fro_status
    

class Kanban(App):
    CSS_PATH = "main.tcss"

    f = open("main.json")
    data = json.load(f)

    counter = process_data(data)

    def on_column_card_moved(self, message):
        delete_card_by_id(self.data, message.fro.id)

        self.data["statuses"][message.to]["cards"].append(message.fro)

        self.refresh(layout=True, recompose=True)

    def on_input_submitted(self) -> None:
        input = self.query_one(Input)
        command = input.value.split()
        input.value = ""
        match command:
            case ["delete_card", card_id]:
                delete_card_by_id(self.data, int(card_id))
            case ["add_card", col_id, text]:
                add_card_by_col_id(self.data, int(col_id), text, self.counter)
                self.counter += 1
            case ["modify_card", card_id, text]:
                modify_card_by_id(self.data, int(card_id), text)
            case ["add_status", status_name]:
                add_status(self.data, status_name)
            case ["swap_status", fro, to]:
                swap_status(self.data, fro, to)
            case _:
                pass

        self.refresh(layout=True, recompose=True)

    def compose(self) -> ComposeResult:
        yield Label(self.data["heading"], id="heading")
        with HorizontalScroll():
                for col, status in enumerate(self.data["statuses"]):
                    with VerticalScroll():
                        yield Label(str(col) + ' - ' + status["title"], classes="status")
                        yield Column(col, status["cards"])

        yield Input(placeholder="Enter a command")


if __name__ == "__main__":
    app = Kanban()
    app.run()
