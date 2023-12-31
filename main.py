import contextlib
import json
import logging
import time

import typer
from binance.error import ClientError
from binance.lib.utils import config_logging
from rich.live import Live

from data.enums import Strategy, TickerSymbol
from display.display import generate_table, layout
from repository.repository import TradeRepo
from strategy.all_price_match_queue import AllPriceMatchQueueStrategy
from strategy.fixed_range import FixedRangeStrategy
from utils.fileutils import get_inputs_from_file

FORMAT = "%(message)s"

# logging.basicConfig(
#     level=logging.INFO,
#     format=FORMAT,
#     datefmt="[%X]",
#     handlers=[RichHandler(markup=True)],
# )
config_logging(logging, logging.ERROR)


def on_message(_, message) -> None:
    data = json.loads(message)
    if "data" in message:
        generate_table(data=data["data"])
        # live.update(renderable=, refresh=True)


def main() -> None:
    live = Live(renderable=layout, refresh_per_second=1, screen=True)
    live.start()
    repo = TradeRepo()
    file_input = get_inputs_from_file()
    listen_key = repo.get_listen_key().listenKey
    ws_client = repo.get_websocket_client(message_handler=on_message, is_combined=True)
    ws_client.user_data(listen_key=listen_key, id=1)
    ws_client.partial_book_depth(symbol=TickerSymbol.BTCUSDT.name, id=2, level=10, speed=100)
    try:
        max_leverage = file_input.leverage
        while True:
            repo.cancel_all_orders(TickerSymbol.BTCUSDT)
            current_leverage = repo.get_position_risk(symbol=file_input.symbol).leverage
            try:
                if max_leverage > current_leverage:
                    repo.change_initial_leverage(file_input.symbol, current_leverage + 1)
                elif max_leverage < current_leverage:
                    repo.change_initial_leverage(file_input.symbol, current_leverage - 1)
            except ClientError as e:
                logging.error(e)
            if file_input.strategy is Strategy.FIXED_RANGE:
                strategy_1 = FixedRangeStrategy(file_input=file_input)
                strategy_1.run_loop()
            elif file_input.strategy is Strategy.PRICE_MATCH_QUEUE:
                strategy_2 = AllPriceMatchQueueStrategy(file_input=file_input)
                strategy_2.run_loop()
            if file_input.once:
                break
            with contextlib.suppress(ClientError):
                repo.keep_alive(listen_key=listen_key)
                ws_client.ping()
            time.sleep(file_input.delay_seconds)
    except Exception as e:
        logging.error(msg=e)
    finally:
        live.stop()
        ws_client.stop()
        repo.close_listen_key(listen_key=listen_key)
        typer.Exit()


if __name__ == "__main__":
    typer.run(function=main)
