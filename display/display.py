import json

from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table

from data.enums import TickerSymbol
from repository.repository import TradeRepo
from utils.timeutils import get_date_and_time


def generate_table(message: str) -> Layout:
    data = json.loads(message) if message else {}
    table = Table()
    table.add_column("ID")
    table.add_column("Value")
    table.add_column("Status")

    repo = TradeRepo()
    open_buy_orders_num = 0
    open_sell_orders_num = 0
    orders = repo.get_open_orders(TickerSymbol.BTCUSDT)
    open_buy_orders_num = sum(order["side"] == "BUY" for order in orders)
    open_sell_orders_num = sum(order["side"] == "SELL" for order in orders)
    mark_price = repo.get_mark_price(TickerSymbol.BTCUSDT)
    last_price = repo.get_ticker_price(TickerSymbol.BTCUSDT)
    entry_price = (
        data["a"]["P"][0]["ep"]
        if message
        else repo.get_position_entry_price(TickerSymbol.BTCUSDT)
    )
    break_even_price = data["a"]["P"][0]["bep"] if message else ""
    accumulated_realized = data["a"]["P"][0]["cr"] if message else ""
    unrealized = data["a"]["P"][0]["up"] if message else repo.get_cross_unrealized()
    position_amount = (
        data["a"]["P"][0]["pa"]
        if message
        else repo.get_hedge_position_amount(TickerSymbol.BTCUSDT)
    )
    wallet_balance = data["a"]["B"][0]["wb"] if message else repo.get_balance()
    liquidation_price = repo.get_liquidation_price(TickerSymbol.BTCUSDT)
    table.add_row("mark_price", f"[green]{mark_price}", get_date_and_time())
    table.add_row("last_price", f"[green]{last_price}")
    table.add_row("entry_price", f"{entry_price}")
    table.add_row("break_even_price", f"{break_even_price}")
    table.add_row("accumulated_realized", f"{accumulated_realized}")
    table.add_row("unrealized", f"{unrealized}", "Liquidation Price")
    table.add_row("position_amount", f"{position_amount}", f"{liquidation_price}")
    table.add_row(
        "wallet_balance",
        f"{wallet_balance}",
        f"{float(wallet_balance)-float(unrealized)}",
    )
    table.add_row(
        "open_buy_orders_num",
        f"{open_buy_orders_num}",
        f"{float(wallet_balance)+float(unrealized)}",
    )
    table.add_row("open_sell_orders_num", f"{open_sell_orders_num}")
    layout = Layout()
    layout.split_row(
        Layout(renderable=Panel(table), name="left"),
        Layout(renderable=Panel("2"), name="right"),
    )
    return layout
