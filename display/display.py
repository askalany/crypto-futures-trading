from rich.align import Align
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table

from data.enums import TickerSymbol
from display.renderables import Footer, Header
from display.utils import f_money, f_pct
from repository.repository import TradeRepo
from utils.timeutils import get_date_and_time


def make_it() -> Layout:
    my_layout = Layout(name="root")
    my_layout.split(
        Layout(name="header", renderable=Header(), size=4),
        Layout(name="main", size=16),
        Layout(name="footer", size=3, renderable=Footer()),
    )
    my_layout["main"].split_row(
        Layout(renderable=Panel("1"), name="left"),
        Layout(renderable=Panel("2", expand=False), name="right"),
    )
    my_layout["left"].split_row(
        Layout(renderable=Panel("1"), name="left_left"),
        Layout(renderable=Panel("2"), name="left_right"),
    )
    my_layout["right"].split_row(
        Layout(renderable=Panel("1"), name="right_left"),
        Layout(renderable=Panel("2"), name="right_right"),
    )

    return my_layout


layout = make_it()


def generate_table(data) -> None:
    if "e" in data:
        if data["e"] in ["ACCOUNT_UPDATE"]:
            data["last_account_updated"] = get_date_and_time()
            display_data_1, display_data_2 = get_display_data(data)
            layout["left_left"].update(
                renderable=Panel(
                    renderable=create_table_1(display_data=display_data_1),
                )
            )
            layout["left_right"].update(
                renderable=Panel(
                    renderable=create_table_1(display_data=display_data_2),
                )
            )

        elif data["e"] in ["depthUpdate"]:
            layout["right_left"].update(
                renderable=Align(
                    Panel(
                        renderable=create_book_side_table(data["b"], "green", "ltr"),
                        title="Bids",
                        expand=False,
                    ),
                    align="right",
                )
            )
            layout["right_right"].update(
                renderable=Align(
                    Panel(
                        renderable=create_book_side_table(data["a"], "red", "rtl"),
                        title="Asks",
                        expand=False,
                    ),
                    align="left",
                )
            )


def create_table_1(display_data) -> Table:
    table = Table(expand=True)
    table.add_column("ID")
    table.add_column("Value")
    {table.add_row(k, v) for k, v in display_data.items()}
    return table


def get_display_data(data) -> tuple[dict[str, str], dict[str, str]]:
    repo = TradeRepo()
    orders = repo.get_open_orders(TickerSymbol.BTCUSDT)
    open_buy_orders_num = sum(order["side"] == "BUY" for order in orders)
    open_sell_orders_num = sum(order["side"] == "SELL" for order in orders)
    mark_price = repo.get_mark_price(TickerSymbol.BTCUSDT).markPrice
    last_price = float(repo.get_ticker_price(TickerSymbol.BTCUSDT))
    position_risk = repo.get_position_risk(TickerSymbol.BTCUSDT)
    account_info = repo.get_account_info()
    entry_price = float(data["a"]["P"][0]["ep"] if data else position_risk.entryPrice)
    break_even_price = float(data["a"]["P"][0]["bep"] if data else 0.0)
    accumulated_realized = float(data["a"]["P"][0]["cr"] if data else 0.0)
    unrealized = float(
        data["a"]["P"][0]["up"] if data else account_info.totalCrossUnPnl
    )
    position_amount = float(
        data["a"]["P"][0]["pa"] if data else position_risk.positionAmt
    )
    wallet_balance = float(
        data["a"]["B"][0]["wb"] if data else account_info.totalWalletBalance
    )
    liquidation_price = position_risk.liquidationPrice
    balance_minus_unrealized = wallet_balance - unrealized
    balance_plus_unrealized = wallet_balance + unrealized
    price_change_mark = mark_price - entry_price
    pnl_mark = price_change_mark * position_amount
    pnl_pct_mark = float(float(price_change_mark / entry_price) * 100.0)
    price_change_last = last_price - entry_price
    pnl_last = price_change_last * position_amount
    pnl_pct_last = float(float(price_change_last / last_price) * 100.0)
    display_data_1 = {
        "mark_price": f_money(mark_price),
        "last_price": f_money(last_price),
        "entry_price": f_money(entry_price),
        "break_even_price": f_money(break_even_price),
        "accumulated_realized": f_money(accumulated_realized),
        "unrealized": f_money(unrealized),
        "position_amount": f"{position_amount}",
        "liquidation_price": f_money(liquidation_price),
        "wallet_balance": f_money(wallet_balance, "yellow"),
        "balance_minus_unrealized-realized": f_money(balance_minus_unrealized),
    }

    display_data_2 = {
        "balance_plus_unrealized": f_money(balance_plus_unrealized),
        "open_buy_orders_num": f"{open_buy_orders_num}",
        "open_sell_orders_num": f"{open_sell_orders_num}",
        "pnl_mark": f_money(pnl_mark),
        "pnl_last": f_money(pnl_last),
        "profit_loss_percentage": f_pct(pnl_pct_mark),
        "profit_loss_percentage_last": f_pct(pnl_pct_last),
    }
    if "last_account_updated" in data:
        display_data_2["last_account_updated"] = data["last_account_updated"]
    return (
        display_data_1,
        display_data_2,
    )


def create_book_side_table(data, color: str, direction: str) -> Table:
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
