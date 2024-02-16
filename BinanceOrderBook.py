from typing import Any

import numpy as np

from data.enums import TickerSymbol
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
