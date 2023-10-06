import concurrent.futures
import logging
import time

import typer
from binance.lib.utils import config_logging
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient
from requests.adapters import HTTPAdapter
from rich import print
from rich.logging import RichHandler

from enums import TIF, PositionSide, Strategy, TickerSymbol
from repo import cancel_all_orders, close_listen_key, get_listen_key
from trade import trade, work
from utils import print_date_and_time

adapter = HTTPAdapter(pool_connections=200, pool_maxsize=200)
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
    listenKey = get_listen_key()
    ws_client = UMFuturesWebsocketClient(on_message=message_handler)
    ws_client.user_data(
        listen_key=listenKey,
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
                positionSide=PositionSide.LONG,
                tif=TIF.GTC,
            )
            with concurrent.futures.ProcessPoolExecutor(max_workers=61) as executor:
                executor.map(work, orders, chunksize=10)
            if once:
                break
            time.sleep(delay_seconds)

    except Exception as e:
        logging.error(msg=e)
    finally:
        ws_client.stop()
        close_listen_key(listenKey=listenKey)


if __name__ == "__main__":
    typer.run(function=main)
