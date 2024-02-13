#!/usr/bin/env python
from __future__ import annotations

import datetime
import math
import random
import sched
import time
from concurrent.futures import ThreadPoolExecutor

import numpy as np

from apirequests import cancel_all_orders, get_client
from apirequests import get_balance
from apirequests import get_position_information
from apirequests import new_market_order
from apirequests import new_order
from base.Settings import Settings
from orderutils import get_optimized_orders
from rich import print


s = sched.scheduler(time.monotonic, time.sleep)


def trade_loop(key, secret):
    get_client(key, secret)
    symbol = "BTCUSD_PERP"
    buy_orders_num = 100
    sell_orders_num = 100
    cancel_all_orders(symbol)
    position_information = get_position_information(symbol=symbol)
    mark_price = float(position_information.markPrice)
    center_price = mark_price
    current_position = float(position_information.positionAmt)
    if current_position <= 0:
        new_market_order(symbol, "BUY", "LONG", 1)
        return
    else:
        center_price = float(position_information.entryPrice)
    fees = 0.07 / 100.0
    center_price = mark_price
    sell_price_max = center_price * 1.1
    sell_price_min = center_price * 1 + fees
    buy_price_max = center_price * 1 - fees
    buy_price_min = center_price * 0.9
    leverage = float(position_information.leverage)
    available_balance = float(get_balance("BTC").availableBalance)
    print(f"available_balance={available_balance}, current_position={current_position}")
    leveraged_available_balance = math.floor(available_balance) * leverage
    min_order = 100.0 / buy_price_max
    optimized_orders = get_optimized_orders(leveraged_available_balance, buy_orders_num, min_order)
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
    print(f"main - {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    key = Settings().KEY
    secret = Settings().SECRET
    keys_and_secrets = [(key, secret)]
    for key, secret in keys_and_secrets:
        trade_loop(key, secret)
    s.enter(900 + (random.random() * 880.0), 1, main)


if __name__ == "__main__":
    s.enter(0, 1, main)
    s.run()
