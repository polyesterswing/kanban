from textual.app import App, ComposeResult
from textual.widgets import Static, ListView, ListItem, Label, Header, Footer, Input
from textual.containers import VerticalScroll, HorizontalScroll, Horizontal, Vertical
from textual.reactive import reactive
from textual.message import Message
from textual.css.query import NoMatches
from textual.screen import Screen
from pathlib import Path
import json

class Card(Label):
    selected = reactive(False)
    card = reactive({"id": 0, "priority": 2, "text": "", "assignee": "", "reporter": ""})

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
        self.border_title = str(self.card["id"])
        self.add_class("card")

    def compose(self) -> ComposeResult:
        if self.card["priority"] == 0:
            self.add_class("high")

        if self.card["priority"] == 1:
            self.add_class("medium")

        if self.card["priority"] == 2:
            self.add_class("low")


        result = ""
        if self.card["assignee"]:
            result += f"[b]Assignee[/b]: {self.card['assignee']}\n"

        if self.card["reporter"]:
            result += f"[b]Reporter[/b]: {self.card['reporter']}\n"

        result += "\n"

        result += self.card["text"]
        yield Label(result)

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
            yield Card(card)

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
            abc = {}
            abc["id"] = counter
            abc["priority"] = card["priority"]
            abc["text"] = card["text"]
            abc["assignee"] = card["assignee"]
            abc["reporter"] = card["reporter"]
            new_cards.append(abc)
            counter += 1

        status["cards"] = new_cards

    return counter

def delete_card_by_id(data, id):
    for status in data["statuses"]:
        for idx, card in enumerate(status["cards"]):
            if card["id"] == id:
                status["cards"].pop(idx)

def add_card_by_col_id(data, id, text, new_id):
    for idx, status in enumerate(data["statuses"]):
        if idx == id:
            new_card = {}
            new_card["id"] = new_id
            new_card["priority"] = 2
            new_card["text"] = text
            new_card["assignee"] = ""
            new_card["reporter"] = ""

            status["cards"].append(new_card)

def modify_card_by_id(data, id, text):
    for status in data["statuses"]:
        for idx, card in enumerate(status["cards"]):
            if card["id"] == id:
                card["text"] = text

def add_status(data, name):
    data["statuses"].append({"title": name, "cards": []})

def delete_status(data, index):
    try:
        removed_status = data["statuses"].pop(index)
        print(f"Deleted status: {removed_status['title']}")
    except IndexError:
        print("Invalid index. No status deleted.")


def swap_status(data, fro, to):
    statuses = data["statuses"]
    to_status = statuses[int(to)].copy()
    fro_status = statuses[int(fro)].copy()

    data["statuses"][int(fro)] = to_status
    data["statuses"][int(to)] = fro_status

def add_assignee(data, id, name):
    for status in data["statuses"]:
        for idx, card in enumerate(status["cards"]):
            if card["id"] == id:
                card["assignee"] = name
    
def add_reporter(data, id, name):
    for status in data["statuses"]:
        for idx, card in enumerate(status["cards"]):
            if card["id"] == id:
                card["reporter"] = name

def add_priority(data, id, priority):
    for status in data["statuses"]:
        for idx, card in enumerate(status["cards"]):
            if card["id"] == id:
                card["priority"] = priority

def save_state(data, file):
    f = open(file, 'w')
    json.dump(data, f, indent=4)
    f.close()

def sort_by_priority(data, rev):
    # 0 -> ascending, 1 -> descending
    rev = False if rev == 0 else True
    for status in data["statuses"]:
        status["cards"].sort(key= lambda x: x["priority"], reverse = rev)

def add_heading(data, name):
    data["heading"] = name

class Kanban(App):
    CSS_PATH = "main.css"

    board_name = input("Enter the name of the board you wish to open: ")
    file_name = board_name + ".json"

    test = {
    "heading": "",
    "statuses": [
        {"title": "To Do", "cards": []},
        {"title": "In Progress", "cards": []},
        {"title": "Done", "cards": []}
    ]
}

        
    file_path = Path(file_name)
    file_path.touch(exist_ok = True)
    f = open(file_path, 'r+')

    try:
        data = json.load(f)
    except json.JSONDecodeError:
        json.dump(test, f, indent=4)
        f.seek(0)
        data = json.load(f)

    counter = process_data(data)

    def on_column_card_moved(self, message):
        delete_card_by_id(self.data, message.fro["id"])

        self.data["statuses"][message.to]["cards"].append(message.fro)

        self.refresh(layout=True, recompose=True)

    def on_input_submitted(self) -> None:
        input = self.query_one(Input)
        command = input.value.split()
        input.value = ""

        if not command:
            return

        match command:
            case ["help"]:
                help_text = (
                    "Available Commands:\n"
                    "- delete_card <card_id>\n"
                    "- add_card <col_id> <text>\n"
                    "- modify_card <card_id> <text>\n"
                    "- add_status <name>\n"
                    "- delete_status <col_id>\n"
                    "- swap_status <col_id> <col_id>\n"
                    "- add_assignee <card_id> <name>\n"
                    "- remove_assignee <card_id>\n"
                    "- add_reporter <card_id> <name>\n"
                    "- remove_reporter <card_id>\n"
                    "- add_priority <card_id> <priority>\n"
                    "- save_state\n"
                    "- sort_priority <reverse>\n"
                    "- add_heading <heading>\n"
                    "- load_board <name>\n"
                )
                self.notify(help_text, title="Help Menu")

            case ["delete_card", card_id]:
                delete_card_by_id(self.data, int(card_id))

            case ["add_card", col_id, *text]:
                card_text = " ".join(text)
                add_card_by_col_id(self.data, int(col_id), card_text, self.counter)
                self.counter += 1

            case ["modify_card", card_id, *text]:
                modify_card_by_id(self.data, int(card_id), " ".join(text))

            case ["add_status", status_name]:
                add_status(self.data, status_name)

            case ["delete_status", col_id]:
                delete_status(self.data, int(col_id))

            case ["swap_status", fro, to]:
                swap_status(self.data, fro, to)

            case ["add_assignee", card_id, name]:
                add_assignee(self.data, int(card_id), name)

            case ["remove_assignee", card_id]:
                add_assignee(self.data, int(card_id), "")

            case ["add_reporter", card_id, name]:
                add_reporter(self.data, int(card_id), name)

            case ["remove_reporter", card_id]:
                add_reporter(self.data, int(card_id), "")

            case ["add_priority", card_id, priority]:
                add_priority(self.data, int(card_id), int(priority))

            case ["save_state"]:
                save_state(self.data, self.file_name)

            case ["sort_priority", reverse]:
                sort_by_priority(self.data, int(reverse))

            case ["add_heading", *heading]:
                add_heading(self.data, " ".join(heading))

            case ["load_board", name]:
                self.file_name = name + ".json"
                test = {"heading": "", "statuses": []}
                    
                file_path = Path(self.file_name)
                file_path.touch(exist_ok = True)
                f = open(file_path, 'r+')

                try:
                    self.data = json.load(f)
                except json.JSONDecodeError:
                    json.dump(test, f, indent=4)
                    f.seek(0)
                    self.data = json.load(f)

                self.counter = process_data(self.data)

            case _:
                self.notify("Invalid command. Type 'help' for a list of available commands.", title="Error")

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
