from rich.align import Align
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table

from data.enums import TickerSymbol
from display.renderables import Footer, Header
from repository.repository import TradeRepo


def make_it():
    layout = Layout(name="root")
    layout.split(
        Layout(name="header", renderable=Header(), size=4),
        Layout(name="main", size=16),
        Layout(name="footer", size=3, renderable=Footer()),
    )
    layout["main"].split_row(
        Layout(renderable=Panel("1"), name="left"),
        Layout(renderable=Panel("2", expand=False), name="right"),
    )
    layout["right"].split_row(
        Layout(renderable=Panel("1"), name="left_1"),
        Layout(renderable=Panel("2"), name="left_2"),
    )

    return layout


layout = make_it()


def generate_table(data):
    if "e" in data:
        if data["e"] in ["ACCOUNT_UPDATE"]:
            layout["left"].update(
                renderable=Panel(renderable=create_table_1(data), title="Account")
            )

        elif data["e"] in ["depthUpdate"]:
            layout["left_1"].update(
                renderable=Align(
                    Panel(
                        renderable=create_book_side_table(data["b"], "green", "ltr"),
                        title="Bids",
                        expand=False,
                    ),
                    align="right",
                )
            )
            layout["left_2"].update(
                renderable=Align(
                    Panel(
                        renderable=create_book_side_table(data["a"], "red", "rtl"),
                        title="Asks",
                        expand=False,
                    ),
                    align="left",
                )
            )


def create_table_1(data):
    table = Table(expand=True)
    table.add_column("ID")
    table.add_column("Value")

    repo = TradeRepo()
    open_buy_orders_num = 0
    open_sell_orders_num = 0
    orders = repo.get_open_orders(TickerSymbol.BTCUSDT)
    open_buy_orders_num = sum(order["side"] == "BUY" for order in orders)
    open_sell_orders_num = sum(order["side"] == "SELL" for order in orders)
    mark_price = float(repo.get_mark_price(TickerSymbol.BTCUSDT))
    last_price = repo.get_ticker_price(TickerSymbol.BTCUSDT)
    entry_price = float(
        data["a"]["P"][0]["ep"]
        if data
        else repo.get_position_entry_price(TickerSymbol.BTCUSDT)
    )
    break_even_price = float(data["a"]["P"][0]["bep"] if data else 0.0)
    accumulated_realized = float(data["a"]["P"][0]["cr"] if data else 0.0)
    unrealized = float(data["a"]["P"][0]["up"] if data else repo.get_cross_unrealized())
    position_amount = (
        data["a"]["P"][0]["pa"]
        if data
        else repo.get_hedge_position_amount(TickerSymbol.BTCUSDT)
    )
    wallet_balance = float(data["a"]["B"][0]["wb"] if data else repo.get_balance())
    liquidation_price = float(repo.get_liquidation_price(TickerSymbol.BTCUSDT))
    balance_minus_unrealized = wallet_balance - unrealized
    balance_plus_unrealized = round(wallet_balance + unrealized)
    table.add_row("mark_price", format_money(mark_price))
    table.add_row("last_price", format_money(last_price))
    table.add_row("entry_price", format_money(entry_price))
    table.add_row("break_even_price", format_money(break_even_price))
    table.add_row("accumulated_realized", format_money(accumulated_realized))
    table.add_row("unrealized", format_money(unrealized))
    table.add_row("position_amount", f"{position_amount}")
    table.add_row("Liquidation", format_money(liquidation_price))
    table.add_row("wallet_balance", format_money(wallet_balance, "yellow"))
    table.add_row("Balance - realized", format_money(balance_minus_unrealized))
    table.add_row("Balance + realized", format_money(balance_plus_unrealized))
    table.add_row("open_buy_orders_num", f"{open_buy_orders_num}")
    table.add_row("open_sell_orders_num", f"{open_sell_orders_num}")
    return table


def format_money(mark_price, color: None | str = None):
    if color is None:
        if mark_price > 0:
            color = "green"
        elif mark_price < 0:
            color = "red"
    return f"[{color}]{'{:,.2f}'.format(mark_price)}"


def create_book_side_table(data, color: str, direction: str):
    table = Table()

    if direction == "ltr":
        table.add_column("Quantity", justify="right")
        table.add_column("Price", justify="right")
        [table.add_row(f"[{color}]{i[1]}", f"[{color}]{i[0]}") for i in data]
    else:
        table.add_column("Price", justify="left")
        table.add_column("Quantity", justify="left")
        [table.add_row(f"[{color}]{i[0]}", f"[{color}]{i[1]}") for i in data]
    return table
