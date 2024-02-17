from itertools import accumulate
from typing import Any

import numpy as np

from data.enums import TickerSymbol
from more_itertools import unzip
from repository.repository import TradeRepo


class BinanceOrderBook:
    def __init__(self, repo: TradeRepo, limit=50):
        self.repo = repo
        self.update(limit)

    def update(self, limit=50):
        self.order_book = self.repo.get_depth(TickerSymbol.BTCUSDT, limit=limit)
        self.bids = self.order_book.bids
        self.asks = self.order_book.asks

    def percentiles(self, x: int = 50) -> tuple[Any, Any]:
        return np.percentile(self.bids, x), np.percentile(self.asks, x)

    def ptps(self) -> tuple[Any, Any]:
        return np.ptp(self.bids), np.ptp(self.asks)

    def largest_volumes_prices(self) -> tuple[float, float]:
        return (
            sorted(self.bids, key=lambda x: x[1], reverse=True)[0][0],
            sorted(self.asks, key=lambda x: x[1], reverse=True)[0][0],
        )

    def volumes(self):
        return np.array(self.bids, dtype=np.float64), np.array(self.asks, dtype=np.float64)

    def centroids(self):
        bids_volumes, asks_volumes = self.volumes()
        return bids_volumes.mean(0)[0], asks_volumes.mean(0)[0]

    def get_accumulated_side(self, side):
        prices, volumes = unzip(side)
        accumulated_volumes = list(accumulate(volumes, lambda x, y: round(x + y, 4)))
        return list(zip(prices, accumulated_volumes))

    def get_accumulated_asks(self):
        return self.get_accumulated_side(self.asks)

    def get_accumulated_bids(self):
        return self.get_accumulated_side(self.bids)

    def get_max_ask(self):
        return max(self.get_accumulated_asks(), key=lambda x: x[1])

    def get_max_bids(self):
        return max(self.get_accumulated_bids(), key=lambda x: x[1])
