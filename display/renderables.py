from datetime import datetime

from rich.panel import Panel
from rich.table import Table

from base.helpers import Singleton
from data.enums import TickerSymbol
from display.utils import f_money
from repository.repository import TradeRepo
from utils.timeutils import get_date_and_time


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


class Footer(metaclass=Singleton):
    def __rich__(self) -> Panel:
        repo = TradeRepo()
        position_risk = repo.get_position_risk(TickerSymbol.BTCUSDT)
        position_amount = float(position_risk["positionAmt"])
        entry_price = float(position_risk["entryPrice"])
        mark_price = float(repo.get_mark_price(TickerSymbol.BTCUSDT).markPrice)
        last_price = float(repo.get_ticker_price(TickerSymbol.BTCUSDT))
        pnl_mark = (mark_price - entry_price) * position_amount
        pnl_last = (last_price - entry_price) * position_amount
        return Panel(
            f"PnL Mark={f_money(pnl_mark)}, PnL Last={f_money(pnl_last)}, Position Amount={position_amount}, Entry Price={f_money(entry_price)}, Mark Price={f_money(mark_price)}, Last Price={f_money(last_price)}, Last Update={get_date_and_time()}",
            title="Footer",
        )
