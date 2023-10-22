from datetime import datetime

from rich.panel import Panel
from rich.table import Table
from base.consts import Settings

from base.helpers import Singleton
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
        orders = repo.get_open_orders(Settings().symbol)
        open_buy_orders_num = sum(order["side"] == "BUY" for order in orders)
        open_sell_orders_num = sum(order["side"] == "SELL" for order in orders)
        position_risk = repo.get_position_risk(Settings().symbol)
        mark_price = repo.get_mark_price(Settings().symbol).markPrice
        last_price = float(repo.get_ticker_price(Settings().symbol))
        pnl_mark = (mark_price - position_risk.entryPrice) * position_risk.positionAmt
        pnl_last = (last_price - position_risk.entryPrice) * position_risk.positionAmt
        return Panel(
            f"OBO={open_buy_orders_num}, OSO={open_sell_orders_num}, LVRG={position_risk.leverage}, PnLMrk={f_money(pnl_mark)}, PnLLst={f_money(pnl_last)}, Ps. Amt.={position_risk.positionAmt}, Ent. Price={f_money(position_risk.entryPrice)}, Mrk Price={f_money(mark_price)}, Lst Price={f_money(last_price)}, Last Update={get_date_and_time()}",
            title="Footer",
        )
