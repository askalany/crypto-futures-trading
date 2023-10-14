from datetime import datetime

from rich.panel import Panel
from rich.table import Table


class Header:
    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "Trading App",
            datetime.now().ctime().replace(":", "[blink]:[/]"),
        )
        return Panel(grid, style="white on blue")


class Left:
    def __init__(self, stuff):
        self.stuff = stuff

    def __rich__(self) -> Panel:
        return Panel(self.stuff, title="Left")


class Right:
    def __init__(self, stuff):
        self.stuff = stuff

    def __rich__(self) -> Panel:
        return Panel(self.stuff, title="Right")


class Footer:
    def __rich__(self) -> Panel:
        return Panel("", title="Footer")
