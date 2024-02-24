# Import necessary libraries and modules
import concurrent.futures
import time

import numpy as np

import requests
from data.enums import PositionSide
from data.enums import Side
from data.enums import TickerSymbol
from repository.repository import TradeRepo  # Replace with the actual API library
from rich import print


def check_internet_connection():
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except requests.exceptions.RequestException:
        return False


class MarketMaker:
    def __init__(self, api_key, api_secret, symbol: TickerSymbol, initial_balance):
        self.exchange = TradeRepo()
        self.symbol = symbol
        self.balance = initial_balance

    def place_limit_order(self, side: Side, quantity: float, position_side: PositionSide, price: float):
        return self.exchange.new_order(
            symbol=self.symbol, side=side, quantity=quantity, position_side=position_side, price=round(price, 1)
        )

    def place_reduce_only_limit_order(self, side: Side, quantity: float, position_side: PositionSide, price: float):
        return self.exchange.new_reduce_only_order(
            symbol=self.symbol, side=side, quantity=quantity, position_side=position_side, price=round(price, 1)
        )

    def cancel_all_orders(self):
        return self.exchange.cancel_all_orders(symbol=self.symbol)

    def get_orderbook(self):
        return self.exchange.book_ticker(self.symbol)

    def mark_price(self):
        return self.exchange.get_mark_price(symbol=self.symbol).markPrice

    def position_amount(self):
        return self.exchange.get_position_risk(self.symbol, position_side=PositionSide.BOTH).positionAmt

    def get_account_balance(self):
        return self.exchange.get_account_balance()

    def execute_market_making_strategy(self):
        forever = True
        turn = 1
        fee = 0.05 / 100.0
        buy_orders_num = 100
        sell_orders_num = 100
        max_position = 10.0
        distance_pct = 1.0
        delay_secs = 20
        order_quantity = round(0.1, 3)
        start_balance = 0.0
        while forever:
            print(f"---round={turn}---")
            if check_internet_connection():
                try:
                    self.cancel_all_orders()
                    orderbook = self.get_orderbook()
                    bid_price = float(orderbook["bidPrice"])
                    ask_price = float(orderbook["askPrice"])
                    mid_price = ((ask_price - bid_price) / 2) + bid_price
                    buy_price = mid_price * (1 - fee)
                    sell_price = mid_price * (1 + fee)
                    position = self.position_amount()
                    account_balance = list(filter(lambda x: x.asset == "USDT", self.get_account_balance()))[0]
                    balance = account_balance.balance
                    if turn == 1:
                        start_balance = balance

                    balance_change = balance - start_balance
                    balance_change_pct = (balance_change / start_balance) * 100
                    availableBalance = account_balance.availableBalance
                    crossWalletBalance = account_balance.crossWalletBalance
                    crossUnPnl = account_balance.crossUnPnl
                    print(f"{mid_price=}, {order_quantity=}, {buy_price=}, {sell_price=}, {position=}")
                    print(f"{balance=}, {availableBalance=}, {crossWalletBalance=}, {crossUnPnl=}")
                    print(f"{balance_change=}, {balance_change_pct=}%")

                    def buy(price: float):
                        self.place_limit_order(
                            side=Side.BUY, quantity=order_quantity, position_side=PositionSide.BOTH, price=price
                        )

                    def sell(price: float):
                        self.place_limit_order(
                            side=Side.SELL, quantity=order_quantity, position_side=PositionSide.BOTH, price=price
                        )

                    def submit_work(work, prices):
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            executor.map(work, prices)

                    buy_price_min = mid_price * (1 - (distance_pct / 100.0))
                    buy_price_max = buy_price
                    sell_price_min = sell_price
                    sell_price_max = mid_price * (1 + (distance_pct / 100.0))
                    buy_prices = np.linspace(buy_price_min, buy_price_max, buy_orders_num)
                    sell_prices = np.linspace(sell_price_min, sell_price_max, num=sell_orders_num)
                    if position < max_position:
                        submit_work(buy, buy_prices)
                    if position > -max_position:
                        submit_work(sell, sell_prices)
                    turn = turn + 1
                    if forever:
                        time.sleep(delay_secs)
                except Exception as e:
                    print(f"An error occurred: {e}")
            else:
                print("No internet connection, waiting for connection...")
                time.sleep(1)  # Adjust sleep time as needed


if __name__ == "__main__":
    api_key = 'your_api_key'
    api_secret = 'your_api_secret'
    symbol = TickerSymbol.BTCUSDT
    initial_balance = 10000

    market_maker = MarketMaker(api_key, api_secret, symbol, initial_balance)
    market_maker.execute_market_making_strategy()
