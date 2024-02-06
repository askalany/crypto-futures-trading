#!/usr/bin/env python
from __future__ import annotations
import math

import time
from concurrent.futures import ThreadPoolExecutor

import numpy as np

from apirequests import cancel_all_orders
from apirequests import get_balance
from apirequests import get_position_information
from apirequests import new_order
from orderutils import get_optimized_orders


def main():
    symbol = "BTCUSD_PERP"
    buy_orders_num = 100
    sell_orders_num = 100
    while True:
        cancel_all_orders(symbol)
        position_information = get_position_information(symbol=symbol)
        mark_price = float(position_information.markPrice)
        sell_price_max = mark_price * 1.05
        sell_price_min = mark_price * 1.005
        buy_price_max = mark_price * 0.995
        buy_price_min = mark_price * 0.95
        current_position = float(position_information.positionAmt)
        leverage = float(position_information.leverage)
        available_balance = math.floor(float(get_balance("BTC").availableBalance)) * leverage
        min_order = 100.0 / buy_price_max
        optimized_orders = get_optimized_orders(available_balance, buy_orders_num, min_order)
        orders = []
        prices = np.linspace(start=buy_price_min, stop=buy_price_max, num=buy_orders_num, dtype=np.float64).tolist()
        j = 99
        for i in optimized_orders:
            buy_price = round(float(prices[j]), 1)
            contract = float(100) / buy_price
            order_amt = round(float(float(i) / contract))
            a = (symbol, "BUY", "LONG", order_amt, buy_price)
            orders.append(a)
            j = j - 1
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
            contract = float(100) / sell_price
            order_amt = round(current_position / float(sell_orders_num))
            a = (symbol, "SELL", "LONG", order_amt, sell_price)
            orders.append(a)
            left_to_sell -= order_amt
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(lambda m: new_order(*m), orders)
        time.sleep(60)


if __name__ == "__main__":
    main()
