import contextlib
import json
import logging
import time

import typer
from binance.error import ClientError
from binance.lib.utils import config_logging
from rich.live import Live
from rich.logging import RichHandler

from data.enums import PositionSide, Strategy, TickerSymbol
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
    (
        once_input,
        use_mark_price_input,
        delay_seconds_input,
        symbol_input,
        strategy_input,
        position_side_input,
        buy_orders_num_input,
        sell_orders_num_input,
        time_in_force_input,
        price_sell_max_mult,
        price_sell_min_mult,
        price_buy_max_mult,
        price_buy_min_mult,
        market_making,
        mm_sell_quantity,
        mm_buy_quantity,
    ) = get_inputs_from_file()
    listen_key = repo.get_listen_key().listenKey
    ws_client = repo.get_websocket_client(
        message_handler=on_message,
        is_combined=True,
    )
    ws_client.user_data(
        listen_key=listen_key,
        id=1,
    )
    ws_client.partial_book_depth(
        symbol=TickerSymbol.BTCUSDT.name,
        id=2,
        level=10,
        speed=100,
    )
    try:
        max_leverage = 2
        while True:
            repo.cancel_all_orders(TickerSymbol.BTCUSDT)
            current_leverage = repo.get_position_risk(symbol=symbol_input).leverage
            try:
                if max_leverage > current_leverage:
                    repo.change_initial_leverage(symbol_input, current_leverage + 1)
                elif max_leverage < current_leverage:
                    repo.change_initial_leverage(symbol_input, current_leverage - 1)
            except ClientError as e:
                logging.error(e)
            if strategy_input is Strategy.FIXED_RANGE:
                strategy_1 = FixedRangeStrategy(
                    symbol=symbol_input,
                    position_side=position_side_input,
                    buy_orders_num=buy_orders_num_input,
                    sell_orders_num=sell_orders_num_input,
                    use_mark_price=use_mark_price_input,
                    time_in_force=time_in_force_input,
                    price_sell_max_mult=price_sell_max_mult,
                    price_sell_min_mult=price_sell_min_mult,
                    price_buy_max_mult=price_buy_max_mult,
                    price_buy_min_mult=price_buy_min_mult,
                    market_making=market_making,
                    mm_sell_quantity=mm_sell_quantity,
                    mm_buy_quantity=mm_buy_quantity,
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
            with contextlib.suppress(ClientError):
                repo.keep_alive(listen_key=listen_key)
                ws_client.ping()
            time.sleep(delay_seconds_input)
    except Exception as e:
        logging.error(msg=e)
    finally:
        live.stop()
        ws_client.stop()
        repo.close_listen_key(listen_key=listen_key)


if __name__ == "__main__":
    typer.run(function=main)
