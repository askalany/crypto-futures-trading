import concurrent.futures
import json
import logging
import time

import typer
from binance.lib.utils import config_logging
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient
from rich.live import Live
from rich.logging import RichHandler
from rich.table import Table

from consts import STREAM_URL
from enums import TickerSymbol
from repo import TradeRepo
from trade import Trade
from utils import batched_lists, get_inputs_from_file

FORMAT = "%(message)s"

logging.basicConfig(
    level=logging.ERROR,
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(markup=True)],
)
config_logging(logging, logging.ERROR)


def generate_table(message: str) -> Table:
    data = json.loads(message) if message else {}
    """Make a new table."""
    table = Table()
    table.add_column("ID")
    table.add_column("Value")
    table.add_column("Status")

    repo = TradeRepo()
    mark_price = repo.get_mark_price(TickerSymbol.BTCUSDT)
    entry_price = data["a"]["P"][0]["ep"] if message else ""
    break_even_price = data["a"]["P"][0]["bep"] if message else ""
    accumulated_realized = data["a"]["P"][0]["cr"] if message else ""
    unrealized = data["a"]["P"][0]["up"] if message else ""
    position_amount = data["a"]["P"][0]["pa"] if message else ""
    wallet_balance = data["a"]["B"][0]["wb"] if message else ""
    table.add_row("mark_price", f"[green]{mark_price}")
    table.add_row("entry_price", f"{entry_price}")
    table.add_row("break_even_price", f"{break_even_price}")
    table.add_row("accumulated_realized", f"{accumulated_realized}")
    table.add_row("unrealized", f"{unrealized}")
    table.add_row("position_amount", f"{position_amount}")
    table.add_row("wallet_balance", f"{wallet_balance}")
    return table


live = Live(generate_table(""), auto_refresh=False)
live.start()


def message_handler(_, message) -> None:
    data = json.loads(message)
    if "e" in data and data["e"] == "ACCOUNT_UPDATE":
        live.update(renderable=generate_table(message=message), refresh=True)


def main() -> None:
    repo = TradeRepo()
    (
        once,
        delay_seconds,
        symbol,
        strategy,
        position_side,
        buy_orders_num,
        sell_orders_num,
        tif,
    ) = get_inputs_from_file()
    listen_key = repo.get_listen_key()
    ws_client = UMFuturesWebsocketClient(
        on_message=message_handler, stream_url=STREAM_URL
    )
    ws_client.user_data(
        listen_key=listen_key,
        id=1,
    )
    try:
        while True:
            # print_date_and_time()
            repo.cancel_all_orders(symbol=symbol)
            mark_price = repo.get_mark_price(symbol=symbol)
            entry_price = repo.get_position_entry_price(symbol=symbol)
            position_amount = repo.get_hedge_position_amount(symbol=symbol)
            trade = Trade(repo=repo)
            orders = trade.trade(
                strategy=strategy,
                symbol=symbol,
                position_side=position_side,
                mark_price=mark_price,
                entry_price=entry_price,
                position_amount=position_amount,
                leverage=repo.get_leverage(symbol=symbol),
                available_balance=repo.get_available_balance(),
                buy_orders_num=buy_orders_num,
                sell_orders_num=sell_orders_num,
                tif=tif,
            )
            batched_orders = batched_lists(orders, 5)
            with concurrent.futures.ProcessPoolExecutor(max_workers=61) as executor:
                executor.map(trade.work, batched_orders, chunksize=5)
            if once:
                break
            repo.keep_alive(listen_key=listen_key)
            time.sleep(delay_seconds)
    except Exception as e:
        logging.error(msg=e)
    finally:
        live.stop()
        ws_client.stop()
        repo.close_listen_key(listen_key=listen_key)


if __name__ == "__main__":
    typer.run(function=main)
