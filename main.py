import concurrent.futures
import logging
import time

import typer
from binance.lib.utils import config_logging
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient
from rich import print
from rich.logging import RichHandler

from enums import PositionSide, Strategy, TickerSymbol, TIF
from repo import cancel_all_orders, close_listen_key, get_listen_key, keep_alive
from trade import trade, work
from utils import batched_lists, print_date_and_time

FORMAT = "%(message)s"

logging.basicConfig(
    level=logging.ERROR,
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(markup=True)],
)
config_logging(logging, logging.ERROR)


def message_handler(_, message) -> None:
    print(message)


def main() -> None:
    delay_seconds = 20
    once = False
    listen_key = get_listen_key()
    ws_client = UMFuturesWebsocketClient(on_message=message_handler)
    ws_client.user_data(
        listen_key=listen_key,
        id=1,
    )
    symbol = TickerSymbol.BTCUSDT
    try:
        while True:
            print_date_and_time()
            cancel_all_orders(symbol=symbol)
            orders = trade(
                strategy=Strategy.FIXED_RANGE,
                symbol=symbol,
                position_side=PositionSide.LONG,
                buy_orders_num=100,
                sell_orders_num=100,
                tif=TIF.GTC,
            )
            print(f"{len(orders)=}")
            batched_orders = batched_lists(orders, 5)
            print(f"{len(batched_orders)=}")
            with concurrent.futures.ProcessPoolExecutor(max_workers=61) as executor:
                executor.map(work, batched_orders, chunksize=5)
            if once:
                break
            else:
                keep_alive(listen_key=listen_key)
                time.sleep(delay_seconds)

    except Exception as e:
        logging.error(msg=e)
    finally:
        ws_client.stop()
        close_listen_key(listen_key=listen_key)


if __name__ == "__main__":
    typer.run(function=main)
