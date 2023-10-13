import json

from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table

from data.enums import TickerSymbol
from repository.repository import TradeRepo
from utils.timeutils import get_date_and_time

table_1 = Table()
table_2 = Table()


def generate_table(data) -> Layout:
    layout = Layout()
    renderable_1 = Panel(table_1)
    renderable_2 = Panel(table_2)
    if "e" in data:
        if data["e"] in ["ACCOUNT_UPDATE"]:
            renderable_1 = Panel(create_table_1(data))
        elif data["e"] in ["depthUpdate"]:
            renderable_2 = Panel(create_table_2(data))
    layout.split_row(
        Layout(renderable=renderable_1, name="left"),
        Layout(renderable=renderable_2, name="right"),
    )
    return layout


def create_table_1(data):
    table_1 = Table()
    table_1.add_column("ID")
    table_1.add_column("Value")
    table_1.add_column("Status")

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
        if data
        else repo.get_position_entry_price(TickerSymbol.BTCUSDT)
    )
    break_even_price = data["a"]["P"][0]["bep"] if data else ""
    accumulated_realized = data["a"]["P"][0]["cr"] if data else ""
    unrealized = data["a"]["P"][0]["up"] if data else repo.get_cross_unrealized()
    position_amount = (
        data["a"]["P"][0]["pa"]
        if data
        else repo.get_hedge_position_amount(TickerSymbol.BTCUSDT)
    )
    wallet_balance = data["a"]["B"][0]["wb"] if data else repo.get_balance()
    liquidation_price = repo.get_liquidation_price(TickerSymbol.BTCUSDT)
    table_1.add_row("mark_price", f"[green]{mark_price}", get_date_and_time())
    table_1.add_row("last_price", f"[green]{last_price}")
    table_1.add_row("entry_price", f"{entry_price}")
    table_1.add_row("break_even_price", f"{break_even_price}")
    table_1.add_row("accumulated_realized", f"{accumulated_realized}")
    table_1.add_row("unrealized", f"{unrealized}", "Liquidation Price")
    table_1.add_row("position_amount", f"{position_amount}", f"{liquidation_price}")
    table_1.add_row(
        "wallet_balance",
        f"{wallet_balance}",
        f"{float(wallet_balance)-float(unrealized)}",
    )
    table_1.add_row(
        "open_buy_orders_num",
        f"{open_buy_orders_num}",
        f"{float(wallet_balance)+float(unrealized)}",
    )
    table_1.add_row("open_sell_orders_num", f"{open_sell_orders_num}")
    return table_1


def create_table_2(data):
    table_2 = Table()
    table_2.add_column("ID")
    table_2.add_column("Value")
    table_2.add_column("Status")
    [table_2.add_row(f"[red]{i[0]}", f"[red]{i[1]}") for i in data["a"]]
    [table_2.add_row(f"[green]{i[0]}", f"[green]{i[1]}") for i in data["b"]]
    return table_2
