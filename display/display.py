from math import remainder
from typing import List

from base.Settings import Settings
from display.renderables import Footer
from display.renderables import Header
from display.utils import f_money
from display.utils import f_pct
from model import BalanceAndPositionUpdate
from model import DepthUpdate
from model import MarkPriceUpdate
from repository.repository import TradeRepo
from rich.align import Align
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from utils.timeutils import get_date_and_time


def make_it() -> Layout:
    my_layout = Layout(name="root")
    my_layout.split(
        Layout(name="header", renderable=Header(), size=4),
        Layout(name="main", size=16),
        Layout(name="footer", size=3, renderable=Footer()),
    )
    my_layout["main"].split_row(
        Layout(renderable=Panel("1"), name="left"), Layout(renderable=Panel("2", expand=False), name="right")
    )
    my_layout["left"].split_row(
        Layout(renderable=Panel("1"), name="left_left"), Layout(renderable=Panel("2"), name="left_right")
    )
    my_layout["right"].split_row(
        Layout(renderable=Panel("1"), name="right_left"), Layout(renderable=Panel("2"), name="right_right")
    )

    return my_layout


layout = make_it()


def generate_table(data) -> None:
    if "e" in data:
        if data["e"] in ["ACCOUNT_UPDATE"]:
            balance_and_position_update = BalanceAndPositionUpdate(**data)
            display_data_1, display_data_2 = get_display_data(balance_and_position_update)
            layout["left_left"].update(renderable=Panel(renderable=create_table_1(display_data=display_data_1)))
            layout["left_right"].update(renderable=Panel(renderable=create_table_1(display_data=display_data_2)))

        elif data["e"] in ["depthUpdate"]:
            depth_update = DepthUpdate(**data)
            layout["right_left"].update(
                renderable=Align(
                    Panel(
                        renderable=create_book_side_table(depth_update.b, "green", "ltr"), title="Bids", expand=False
                    ),
                    align="right",
                )
            )
            layout["right_right"].update(
                renderable=Align(
                    Panel(renderable=create_book_side_table(depth_update.a, "red", "rtl"), title="Asks", expand=False),
                    align="left",
                )
            )
        elif data["e"] in ["markPriceUpdate"]:
            mark_price_update = MarkPriceUpdate(**data)


def create_table_1(display_data: dict) -> Table:
    table = Table(expand=True)
    table.add_column("ID")
    table.add_column("Value")
    for k, v in display_data.items():
        table.add_row(k, v)
    return table


def get_display_data(balance_and_position_update: BalanceAndPositionUpdate) -> tuple[dict[str, str], dict[str, str]]:
    repo = TradeRepo()
    mark_price = repo.get_mark_price(Settings().file_input.symbol).markPrice
    last_price = float(repo.get_ticker_price(Settings().file_input.symbol))
    position_risk = repo.get_position_risk(Settings().file_input.symbol)
    a = balance_and_position_update.a.P[0].ep
    p_0 = balance_and_position_update.a.P[0]
    b_0 = balance_and_position_update.a.B[0]
    entry_price = float(p_0.ep)
    break_even_price = float(p_0.bep)
    accumulated_realized = float(p_0.cr)
    unrealized = float(p_0.up)
    position_amount = float(p_0.pa)
    wallet_balance = float(b_0.wb)
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
        "pnl_mark": f_money(pnl_mark),
        "pnl_last": f_money(pnl_last),
        "profit_loss_percentage": f_pct(pnl_pct_mark),
        "profit_loss_percentage_last": f_pct(pnl_pct_last),
    }
    display_data_2["last_account_updated"] = get_date_and_time()
    return (display_data_1, display_data_2)


def create_book_side_table(book_side: List[List[str]], color: str, direction: str) -> Table:
    table = Table()

    if direction == "ltr":
        table.add_column("Quantity", justify="right")
        table.add_column("Price", justify="right")
        for k, v in compress_book(book_side, 10).items():
            table.add_row(f"[{color}]{v}", f"[{color}]{k}")
    else:
        table.add_column("Price", justify="left")
        table.add_column("Quantity", justify="left")
        for k, v in compress_book(book_side, 10).items():
            table.add_row(f"[{color}]{k}", f"[{color}]{v}")
    return table


def round_up_to(price, up_to) -> float:
    p = float(price)
    rem = remainder(p, up_to)
    return p + 100.0 - rem if rem > 0.0 else p + abs(rem)


def compress_book(book: list[list[str]], up_to):
    result: dict[float, float] = {}
    for b in book:
        p = round_up_to(b[0], up_to)
        result[p] = round(result[p] + float(b[1]) if p in result else float(b[1]), 4)
    return result
