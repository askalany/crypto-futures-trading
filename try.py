# Import necessary libraries and modules
import concurrent.futures
import datetime
import time

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

import requests
import typer
from data.enums import PositionSide
from data.enums import Side
from data.enums import TickerSymbol
from repository.repository import TradeRepo  # Replace with the actual API library
from rich import print
from utils.fileutils import get_db_from_file
from utils.fileutils import write_to_db_file


def vol(amount):
    return '[bold blue]{:,.4f} USDT[/bold blue]'.format(amount)


def price(amount):
    return '[bold blue]{:,.1f} USDT[/bold blue]'.format(amount)


def money(amount):
    if amount > 0:
        return '[bold green]{:,.2f} USDT[/bold green]'.format(amount)
    elif amount < 0:
        return '[bold red]-{:,.2f} USDT[/bold red]'.format(-amount)
    else:
        return '[bold blue]{:,.2f} USDT[/bold blue]'.format(amount)


def pct(amount):
    if amount > 0:
        return '[bold green]{:}%[/bold green]'.format(amount)
    elif amount < 0:
        return '[bold red]-{:}%[/bold red]'.format(-amount)
    else:
        return '[bold blue]{:}%[/bold blue]'.format(amount)


def calculate_apy(initial_balance, current_balance, start_time, current_time):
    """
    Calculates the APY (Annual Percentage Yield) given the initial balance, current balance, start time, and current time.

    Args:
        initial_balance: The initial balance of the investment.
        current_balance: The current balance of the investment.
        start_time: The start time of the investment as a datetime object.
        current_time: The current time as a datetime object.

    Returns:
        The APY as a float.
    """

    # Ensure start_time and current_time are datetime objects
    if not isinstance(start_time, datetime.datetime):
        start_time = datetime.datetime.fromisoformat(start_time)
    if not isinstance(current_time, datetime.datetime):
        current_time = datetime.datetime.fromisoformat(current_time)

    # Calculate the time difference in years
    time_delta = current_time - start_time
    total_years = time_delta.total_seconds() / (365.25 * 24 * 60 * 60)

    # Calculate the return on investment (ROI)
    roi = (current_balance - initial_balance) / initial_balance

    # If there is no change in balance, APY is 0%
    if roi == 0:
        return 0

    # Calculate and return the APY as a percentage
    apy = (1 + roi) ** (1 / total_years) - 1
    return round(apy * 100, 2)


def calculate_dpy(initial_balance, current_balance, start_time, current_time):
    """
    Calculates the Daily Percentage Yield (DPY) given the initial balance, current balance, start time, and current time.

    Args:
        initial_balance: The initial balance of the investment.
        current_balance: The current balance of the investment.
        start_time: The start time of the investment as a datetime object.
        current_time: The current time as a datetime object.

    Returns:
        The DPY as a float.
    """

    # Ensure start_time and current_time are datetime objects
    if not isinstance(start_time, datetime.datetime):
        start_time = datetime.datetime.fromisoformat(start_time)
    if not isinstance(current_time, datetime.datetime):
        current_time = datetime.datetime.fromisoformat(current_time)

    # Calculate the time difference in days
    time_delta = current_time - start_time
    total_days = time_delta.total_seconds() / (24 * 60 * 60)

    # Calculate the rest of the function as per the existing logic, replacing years with days
    roi = (current_balance - initial_balance) / initial_balance
    if roi == 0:
        return 0
    dpy = (1 + roi) ** (1 / total_days) - 1
    return round(dpy * 100, 2)


def calculate_mpy(initial_balance, current_balance, start_time, current_time):
    """
    Calculates the Monthly Percentage Yield (MPY) given the initial balance, current balance, start time, and current time.

    Args:
        initial_balance: The initial balance of the investment.
        current_balance: The current balance of the investment.
        start_time: The start time of the investment as a datetime object.
        current_time: The current time as a datetime object.

    Returns:
        The MPY as a float.
    """

    # Ensure start_time and current_time are datetime objects
    if not isinstance(start_time, datetime.datetime):
        start_time = datetime.datetime.fromisoformat(start_time)
    if not isinstance(current_time, datetime.datetime):
        current_time = datetime.datetime.fromisoformat(current_time)

    # Calculate the time difference in months
    time_delta = current_time - start_time
    total_months = (time_delta.total_seconds() / (365.25 * 24 * 60 * 60)) * 12

    # Calculate the rest of the function as per the existing logic, replacing years with months
    roi = (current_balance - initial_balance) / initial_balance
    if roi == 0:
        return 0
    mpy = (1 + roi) ** (1 / total_months) - 1
    return round(mpy * 100, 2)


def check_internet_connection():
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except requests.exceptions.RequestException:
        return False


class MarketMaker:
    def __init__(self, symbol: TickerSymbol):
        self.exchange = TradeRepo()
        self.symbol = symbol
        self.dpy_history = []
        self.max_size = 10
        self.max_quantity = 1
        self.min_quantity = 0.003
        self.order_size = 0.5  # initial order size

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

    def train_ml_model(self):
        # Train a simple ML model based on historical APY data
        X = np.arange(len(self.dpy_history)).reshape(-1, 1)
        y = np.array(self.dpy_history)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = LinearRegression()
        model.fit(X_train, y_train)

        return model

    def optimize_order_size(self):
        # Get the trained ML model
        model = self.train_ml_model()

        # Predict APY for the next time step
        next_dpy = model.predict([[len(self.dpy_history)]])[0]
        print(f"next_dpy={pct(round(next_dpy * 100,2))}")

        # Adjust order size based on predicted APY (replace with your own logic)
        if next_dpy > self.dpy_history[-1]:
            self.order_size += 0.001
        else:
            self.order_size -= 0.001

        # Ensure order size is within acceptable limits
        self.order_size = round(max(self.min_quantity, min(self.order_size, self.max_quantity)), 3)

    def execute_market_making_strategy(self):
        forever = True
        turn = 1
        fee = 0.05 / 100.0
        buy_orders_num = 100
        sell_orders_num = 100
        distance_pct = 0.5
        delay_secs = 60
        start_balance = get_db_from_file().balance
        start_time = datetime.datetime.now()

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
                    if turn == 1 and start_balance == 0.0:
                        start_balance = balance
                    write_to_db_file(balance)
                    current_time = datetime.datetime.now()
                    dpy = calculate_dpy(start_balance, balance, start_time, current_time)
                    mpy = calculate_mpy(start_balance, balance, start_time, current_time)
                    apy = calculate_apy(start_balance, balance, start_time, current_time)
                    balance_change = round(balance - start_balance, 0)
                    balance_change_pct = round((balance_change / start_balance) * 100, 2)
                    availableBalance = account_balance.availableBalance
                    crossWalletBalance = account_balance.crossWalletBalance
                    crossUnPnl = account_balance.crossUnPnl

                    print(
                        f"mid_price={price(mid_price)}, order_quantity={vol(self.order_size)}, buy_price={price(buy_price)}, sell_price={price(sell_price)}, position={vol(position)}"
                    )
                    print(
                        f"balance={money(balance)}, availableBalance={money(availableBalance)}, crossWalletBalance={money(crossWalletBalance)}, crossUnPnl={money(crossUnPnl)}"
                    )
                    print(
                        f"balance_change={money(balance_change)}, balance_change_pct={pct(balance_change_pct)}, dpy={pct(dpy)}, mpy={pct(mpy)}, apy={pct(apy)}"
                    )

                    def buy(price: float):
                        self.place_limit_order(
                            side=Side.BUY, quantity=self.order_size, position_side=PositionSide.BOTH, price=price
                        )

                    def sell(price: float):
                        self.place_limit_order(
                            side=Side.SELL, quantity=self.order_size, position_side=PositionSide.BOTH, price=price
                        )

                    def submit_work(work, prices):
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            executor.map(work, prices)

                    buy_price_min = mid_price * (1 - (distance_pct / 100.0))
                    buy_price_max = buy_price
                    sell_price_min = sell_price
                    sell_price_max = mid_price * (1 + (distance_pct / 100.0))
                    buy_prices = np.linspace(buy_price_max, buy_price_min, buy_orders_num)
                    sell_prices = np.linspace(sell_price_min, sell_price_max, sell_orders_num)
                    if position < self.max_size:
                        submit_work(buy, buy_prices)
                    if position > -self.max_size:
                        submit_work(sell, sell_prices)
                    turn = turn + 1
                    self.dpy_history.append(dpy / 100)
                    self.optimize_order_size()
                    print(f"Order size: {self.order_size}, DPY: {pct(round(self.dpy_history[-1]*100,2))}")
                    if forever:
                        time.sleep(delay_secs)
                except Exception as e:
                    print(f"An error occurred: {e}")
            else:
                print("No internet connection, waiting for connection...")
                time.sleep(1)  # Adjust sleep time as needed


def main():
    symbol = TickerSymbol.BTCUSDT
    MarketMaker(symbol).execute_market_making_strategy()


if __name__ == "__main__":
    typer.run(main)
