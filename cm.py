#!/usr/bin/env python
from __future__ import annotations

import datetime
from itertools import dropwhile, repeat
import math
import random
import sched
import time
from concurrent.futures import ThreadPoolExecutor

import numpy as np

from cm.apirequests import cancel_all_orders, get_account, get_client, get_depth
from cm.apirequests import get_balance
from cm.apirequests import get_position_information
from cm.apirequests import new_market_order
from cm.apirequests import new_order
from base.Settings import Settings
from cm.orderutils import get_optimized_orders
from rich import print


sc = sched.scheduler(time.monotonic, time.sleep)


def trade_loop(key, secret, order_book):
    get_client(key, secret)
    symbol = "BTCUSD_PERP"
    bids = order_book.bids
    bids_volumes = np.array(bids)
    bids_centroid = bids_volumes.mean(0)[0]
    asks = order_book.asks
    asks_volumes = np.array(asks)
    asks_centroid = asks_volumes.mean(0)[0]
    buy_orders_num = 100
    sell_orders_num = 100
    position_information = get_position_information(symbol=symbol)
    mark_price = float(position_information.markPrice)
    center_price = mark_price  # ((asks_centroid - bids_centroid) / 2.0) + bids_centroid
    current_position = float(position_information.positionAmt)
    if current_position <= 0:
        new_market_order(symbol, "BUY", "LONG", 1)
        return
    else:
        center_price = float(position_information.entryPrice)
    fees = 0.07 / 100.0
    distance = 2 * fees
    center_price = mark_price
    sell_price_max = center_price * 1.2  # asks_centroid
    sell_price_min = center_price * (1 + fees)
    buy_price_max = center_price * (1 - fees)
    buy_price_min = center_price * 0.8  # bids_centroid
    leverage = float(position_information.leverage)
    available_balance = float(get_balance("BTC").availableBalance)
    wallet_balance = list(filter(lambda x: x.asset == "BTC", get_account().assets))[0].walletBalance
    print(f"available_balance={available_balance}, current_position={current_position}, {wallet_balance=}")
    leveraged_available_balance = math.floor(available_balance) * leverage
    min_order = 100.0 / buy_price_max
    optimized_orders = get_optimized_orders(leveraged_available_balance, buy_orders_num, min_order)
    optimized_orders = repeat(leveraged_available_balance / 100.0, 100)
    orders = []
    prices = np.linspace(start=buy_price_min, stop=buy_price_max, num=buy_orders_num, dtype=np.float64).tolist()
    for order, price in zip(optimized_orders, reversed(prices)):
        buy_price = round(float(price), 1)
        contract_amount = 100.0 / buy_price
        order_amt = round(order / contract_amount)
        orders.append((symbol, "BUY", "LONG", order_amt, buy_price))
    sell_orders_num = sell_orders_num if current_position >= 200 else int(current_position)
    sell_prices = np.linspace(
        start=sell_price_min,
        stop=sell_price_max,
        num=sell_orders_num if current_position >= 200 else int(current_position),
        dtype=np.float64,
    ).tolist()
    left_to_sell = current_position
    for sell_price in sell_prices:
        if left_to_sell <= 0.0:
            break
        contract_amount = 100.0 / sell_price
        order_amt = round(current_position / float(sell_orders_num))
        orders.append((symbol, "SELL", "LONG", order_amt, round(sell_price, 1)))
        left_to_sell -= order_amt
    with ThreadPoolExecutor() as executor:
        executor.map(lambda m: new_order(*m), orders, chunksize=5)


def main():
    once = False
    print(f"main - {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    key = Settings().KEY
    secret = Settings().SECRET
    key_1 = ""
    secret_1 = ""
    keys_and_secrets = [(key_1, secret_1), (key, secret)]
    for k, s in keys_and_secrets:
        get_client(k, s)
        cancel_all_orders("BTCUSD_PERP")
    get_client(key, secret)
    order_book = get_depth("BTCUSD_PERP", limit=50)
    for k, s in keys_and_secrets:
        trade_loop(k, s, order_book)
    if not once:
        random_secs = 0.0  # 880.0
        sc.enter(delay=3600 + (random.random() * random_secs), priority=1, action=main)


if __name__ == "__main__":
    sc.enter(0, 1, main)
    sc.run()
