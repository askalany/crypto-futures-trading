import json
import logging
import time

import typer
from base.Settings import Settings
from binance.lib.utils import config_logging
from binance.websocket.binance_socket_manager import BinanceSocketManager
from data.enums import Strategy
from display.display import generate_table
from display.display import layout
from repository.repository import TradeRepo
from rich.live import Live

# from rich.logging import RichHandler
from strategy.all_price_match_queue import AllPriceMatchQueueStrategy
from strategy.fixed_range import FixedRangeStrategy
from base.Settings import Settings
from binance.lib.utils import config_logging
from binance.websocket.binance_socket_manager import BinanceSocketManager
from data.enums import Strategy
from display.display import generate_table
from display.display import layout
from repository.repository import TradeRepo
from rich.live import Live
from strategy.all_price_match_queue import AllPriceMatchQueueStrategy
from strategy.fixed_range import FixedRangeStrategy

FORMAT = "%(message)s"

# logging.basicConfig(level=logging.ERROR, format=FORMAT, datefmt="[%X]", handlers=[RichHandler(markup=True)])
config_logging(logging, logging.ERROR)


def on_message(ws, message) -> None:
    data = json.loads(message)
    if "data" in message:
        generate_table(data=data["data"])
        # live.update(renderable=, refresh=True)


def on_ping(ws: BinanceSocketManager, arg2):
    ws.ping()
    TradeRepo().keep_alive(listen_key=TradeRepo().get_listen_key().listenKey)


def main() -> None:
    live = Live(renderable=layout, refresh_per_second=1, screen=True)
    live.start()
    repo = TradeRepo()
    listen_key = repo.get_listen_key().listenKey
    ws_client = repo.get_websocket_client(message_handler=on_message, on_ping=on_ping, is_combined=True)
    ws_client.user_data(listen_key=listen_key, id=1)
    ws_client.partial_book_depth(symbol=Settings().file_input.symbol.name, id=2, level=20, speed=100)
    ws_client.mark_price(symbol="btcusdt", id=13, speed=1)
    max_leverage = Settings().file_input.leverage
    while True:
        try:
            repo.cancel_all_orders(Settings().file_input.symbol)
            current_leverage = repo.get_position_risk(symbol=Settings().file_input.symbol).leverage
            if max_leverage > current_leverage:
                repo.change_initial_leverage(Settings().file_input.symbol, current_leverage + 1)
            elif max_leverage < current_leverage:
                repo.change_initial_leverage(Settings().file_input.symbol, current_leverage - 1)
            strategy = Settings().file_input.strategy
            if strategy is Strategy.FIXED_RANGE:
                FixedRangeStrategy().run_loop()
            elif strategy is Strategy.PRICE_MATCH_QUEUE:
                AllPriceMatchQueueStrategy().run_loop()
            if Settings().file_input.once:
                break
            time.sleep(Settings().file_input.delay_seconds)
        except Exception as e:
            logging.error(e)
            continue


if __name__ == "__main__":
    config_logging(logging, logging.ERROR)
    typer.run(main)


if __name__ == "__main__":
    typer.run(function=main)
