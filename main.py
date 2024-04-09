from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.reactive import Reactive
from rich.console import RenderableType
from rich.padding import Padding
from rich.align import Align
from rich.text import Text
from rich.table import Table, box
from rich.panel import Panel
from textual.widgets import Footer, Label, ListItem, ListView

class Card(Widget):
    def compose(self) -> ComposeResult:
        yield

class Grid(Widget):
    table = Table(title="Jobs", expand=True, show_lines=False, box=box.SIMPLE_HEAD)

    table.add_column("Todo", ratio=1)
    table.add_column("Doing", ratio=1)
    table.add_column("Done", ratio=1)

    table1 = Table.grid(expand = True)
    table2 = Table.grid(expand = True)
    table3 = Table.grid(expand = True)

    table1.add_row(
        Panel("Find out why the component doesnt work?", border_style="blue"),
    )
    table1.add_row(
        Panel("Fix the Component", border_style="blue"),
    )

    table2.add_row(
        Panel("ABC", border_style="green"),
    )

    table3.add_row(
        Panel("ABC", border_style="red"),
    )


    table.add_row(
            table1,
            table2,
            table3,
    )

    def render(self) -> RenderableType:
        return self.table

class MainApp(App):

    def compose(self) -> ComposeResult:
        yield Grid()

MainApp().run()
