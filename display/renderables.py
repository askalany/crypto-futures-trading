from datetime import datetime

from rich.panel import Panel
from rich.table import Table
from base.Settings import Settings

from base.Singleton import Singleton
from display.utils import f_money
from repository.repository import TradeRepo
from utils.timeutils import get_date_and_time


class Header:
    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row("Trading App", datetime.now().ctime().replace(":", "[blink]:[/]"))
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
        symbol = Settings().file_input.symbol
        orders = repo.get_open_orders(symbol)
        position_risk = repo.get_position_risk(symbol)
        mark_price = repo.get_mark_price(symbol).markPrice
        last_price = float(repo.get_ticker_price(symbol))
        return Panel(
            f"OBO={sum(order['side'] == 'BUY' for order in orders)}, OSO={sum(order['side'] == 'SELL' for order in orders)}, LVRG={position_risk.leverage}, PnLMrk={f_money((mark_price - position_risk.entryPrice) * position_risk.positionAmt)}, PnLLst={f_money((last_price - position_risk.entryPrice) * position_risk.positionAmt)}, Ps. Amt.={position_risk.positionAmt}, Ent. Price={f_money(position_risk.entryPrice)}, Mrk Price={f_money(mark_price)}, Lst Price={f_money(last_price)}, Last Update={get_date_and_time()}",
            title="Footer",
        )
