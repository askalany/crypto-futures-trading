from itertools import count
import json
from statistics import harmonic_mean, mean, median, median_high, median_low, mode
from BinanceOrderBook import BinanceOrderBook
from data.enums import TickerSymbol
from model import DepthUpdate, OrderBook
from repository.repository import TradeRepo
from rich import print
import numpy as np
import time
import logging
from binance.lib.utils import config_logging
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient
from binance.um_futures import UMFutures
import threading
import queue

from collections import deque

config_logging(logging, logging.ERROR)

depth = None

q = queue.Queue()


def worker():
    while True:
        item = q.get()
        print(f'Working on {item}')
        print(f'Finished {item}')
        q.task_done()


def message_handler(_, message):
    q.put(DepthUpdate(**json.loads(message)))


um_futures_client = UMFutures()


def main():
    threading.Thread(target=worker, daemon=True).start()
    my_client = UMFuturesWebsocketClient(on_message=message_handler)
    # 1.Open a stream to wss://fstream.binance.com/stream?streams=btcusdt@depth.
    my_client.diff_book_depth(symbol="btcusdt", speed=100, id=1)
    # 2. Buffer the events you receive from the stream. For same price, latest received update covers the previous one.
    # 3. Get a depth snapshot from https://fapi.binance.com/fapi/v1/depth?symbol=BTCUSDT&limit=1000.
    global depth
    depth = OrderBook(**um_futures_client.depth("BTCUSDT", **{"limit": 1000}))
    # print(f"{depth=}")
    # 4. Drop any event where u is < lastUpdateId in the snapshot.
    # 5. The first processed event should have U <= lastUpdateId AND u >= lastUpdateId
    # 6. While listening to the stream, each new event's pu should be equal to the previous event's u, otherwise initialize the process from step 3.
    # 7. The data in each event is the absolute quantity for a price level.
    # 8. If the quantity is 0, remove the price level.
    # 9. Receiving an event that removes a price level that is not in your local order book can happen and is normal.

    q.join()
    #time.sleep(10)
    logging.debug("closing ws connection")
    my_client.stop()
    print('All work completed')


if __name__ == "__main__":
    main()


def trade():
    print("try")
    repo = TradeRepo(testnet=False)
    binance_order_book = BinanceOrderBook(repo, symbol=TickerSymbol.BTCUSDT, limit=50)
    (balanced_ask_price, balanced_bid_price) = binance_order_book.get_balanced_prices()
    balanced_prices_center = (balanced_ask_price + balanced_bid_price) / 2.0
    print(f"{balanced_ask_price=}, {balanced_prices_center=}, {balanced_bid_price=}")
    (asks_centroid, bids_centroid) = binance_order_book.centroids()
    centroids_center = binance_order_book.get_centroids_center_price()
    print(f"{asks_centroid=}, {centroids_center=}, {bids_centroid=}")
    absolute_center_price = binance_order_book.get_absolute_center_price()
    print(f"{absolute_center_price=}")
    (mean_max, mean_center, mean_min) = binance_order_book.get_all_means()
    mark_price = binance_order_book.get_mark_price()
    print(f"{mark_price=}")
    print(f"{mean_max=}, {mean_center=}, {mean_min=}")
    print(f"{mean([mean_max, mark_price])=}, {mean([mean_center, mark_price])=}, {mean([mean_min, mark_price])=}")
    ask_prices = [x[0] for x in binance_order_book.asks]
    bid_prices = [x[0] for x in binance_order_book.bids]
    asks_harmonic_mean = harmonic_mean(ask_prices)
    bids_harmonic_mean = harmonic_mean(bid_prices)
    asks_median_high = median_high(ask_prices)
    bids_median_low = median_low(bid_prices)
    asks_mean = mean(ask_prices)
    bids_mean = mean(bid_prices)
    asks_median = median(ask_prices)
    bids_median = median(bid_prices)
    asks_mode = mode(ask_prices)
    bids_mode = mode(bid_prices)
    print(f"{asks_harmonic_mean=}, {bids_harmonic_mean=}")
    print(f"{asks_median_high=}, {bids_median_low=}")
    print(f"{asks_mean=}, {bids_mean=}")
    print(f"{asks_median=}, {bids_median=}")
    print(f"{asks_mode=}, {bids_mode=}")
