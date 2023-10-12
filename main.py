# pylint: disable=missing-docstring
import json
import logging
import time

import typer
from binance.lib.utils import config_logging
from rich.live import Live
from rich.logging import RichHandler

from data.enums import PositionSide, Strategy, TickerSymbol
from display.display import generate_table
from repository.repository import TradeRepo
from strategy.all_price_match_queue import AllPriceMatchQueueStrategy
from strategy.fixed_range import FixedRangeStrategy
from utils.utils import get_inputs_from_file

FORMAT = "%(message)s"

logging.basicConfig(
    level=logging.ERROR,
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(markup=True)],
)
config_logging(logging, logging.ERROR)

live = Live(generate_table(""), auto_refresh=False)
live.start()


def message_handler(_, message) -> None:
    data = json.loads(message)
    if "e" in data and data["e"] == "ACCOUNT_UPDATE":
        live.update(renderable=generate_table(message=message), refresh=True)


def main() -> None:
    repo = TradeRepo()
    (
        once_input,
        use_mark_price_input,
        delay_seconds_input,
        symbol_input,
        strategy_input,
        position_side_input,
        buy_orders_num_input,
        sell_orders_num_input,
        tif_input,
        price_sell_max_mult,
        price_sell_min_mult,
        price_buy_max_mult,
        price_buy_min_mult,
    ) = get_inputs_from_file()
    listen_key = repo.get_listen_key()
    ws_client = repo.get_websocket_client(message_handler=message_handler)
    ws_client.user_data(
        listen_key=listen_key,
        id=1,
    )
    try:
        while True:
            if strategy_input is Strategy.FIXED_RANGE:
                strategy_1 = FixedRangeStrategy(
                    symbol=symbol_input,
                    position_side=position_side_input,
                    use_mark_price=use_mark_price_input,
                    price_sell_max_mult=price_sell_max_mult,
                    price_sell_min_mult=price_sell_min_mult,
                    price_buy_max_mult=price_buy_max_mult,
                    price_buy_min_mult=price_buy_min_mult,
                )
                strategy_1.run_loop()
            elif strategy_input is Strategy.PRICE_MATCH_QUEUE:
                strategy_2 = AllPriceMatchQueueStrategy(
                    symbol=TickerSymbol.BTCUSDT,
                    position_side=PositionSide.LONG,
                )
                strategy_2.run_loop()
            if once_input:
                break
            repo.keep_alive(listen_key=listen_key)
            live.update(renderable=generate_table(message=""), refresh=True)
            time.sleep(delay_seconds_input)
    except Exception as e:
        logging.error(msg=e)
    finally:
        live.stop()
        ws_client.stop()
        repo.close_listen_key(listen_key=listen_key)


if __name__ == "__main__":
    typer.run(function=main)
