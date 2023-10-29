import numpy as np

import plotext as plt


class GridTradingBot:
    def __init__(
        self,
        symbol,
        start_price: float,
        lowest_price: float,
        highest_price: float,
        grid_count: int,
        balance: float,
        quantity_per_grid: float,
    ):
        self.symbol = symbol
        self.price: float = start_price
        self.grid_count = grid_count
        self.grid_spacing = (highest_price - lowest_price) / (grid_count - 1)
        self.balance: float = balance
        self.grids: dict[str, dict[str, float]] = {}
        self.quantity: float = 0.0
        self.quantity_per_grid = quantity_per_grid
        self.lowest_price = lowest_price
        self.highest_price = highest_price

    def initialize_grids(self):
        for i in range(self.grid_count):
            price = self.lowest_price + (i * self.grid_spacing)
            self.grids[f"{price}"] = {"price": price, "quantity": 0.0}

    def buy(self, price: float):
        self.quantity += self.quantity_per_grid
        self.balance -= price * self.quantity_per_grid
        return {"price": price, "quantity": self.quantity_per_grid}

    def sell(self, price: float):
        self.quantity -= self.quantity_per_grid
        self.balance += price * self.quantity_per_grid
        return {"price": price, "quantity": 0.0}

    def simulate_price_movement(self):
        price_diff = float(np.random.normal(0, 1))  # Simulate price movement with a normal distribution
        self.price += price_diff * 10
        return self.price

    def execute_trade(self):
        for k, v in self.grids.items():
            if v['quantity'] == 0.0 and self.price <= v["price"]:
                self.grids[k] = self.buy(self.price)
            elif v['quantity'] != 0.0 and self.price >= v["price"]:
                self.grids[k] = self.sell(self.price)

    def run(self, num_ticks: int):
        self.initialize_grids()
        prices = [self.price]
        balance = [self.balance]
        for _ in range(num_ticks):
            self.simulate_price_movement()
            self.execute_trade()
            prices.append(self.price)
            balance.append(self.balance)
            plt.ylim(lower=self.lowest_price, upper=self.highest_price, yside=1)
            plt.clt()
            plt.cld()
            plt.scatter(prices)
            [plt.horizontal_line(v["price"], color='green') for k, v in self.grids.items()]
            plt.xlabel("Time")
            plt.ylabel("Price/Levels")
            plt.title("Price and Grid Levels")
            plt.sleep(0.1)
            plt.show()
        print(f"{self.balance=}")
        print(f"{self.quantity=}")

        # print(f"Balance: {self.balance:.2f} | Current Price: {self.price:.2f}")


if __name__ == "__main__":
    bot = GridTradingBot(
        symbol="BTC",
        start_price=34000.0,
        lowest_price=30000.0,
        highest_price=40000.0,
        grid_count=200,
        balance=60000000.0,
        quantity_per_grid=0.01,
    )
    bot.run(num_ticks=100)
