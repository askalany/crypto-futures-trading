from typing import Any
import numpy as np

from data.enums import TickerSymbol
from repository.repository import TradeRepo


class BinanceOrderBook:
    def __init__(self, repo: TradeRepo, symbol: TickerSymbol, limit=50):
        self.repo = repo
        self.symbol = symbol
        self.update(limit)

    def update(self, limit=50):
        self.mark_price = self.repo.get_mark_price(self.symbol).markPrice
        self.order_book = self.repo.get_depth(self.symbol, limit=limit)
        self.asks = np.array(self.order_book.asks, dtype=np.float64)
        self.bids = np.array(self.order_book.bids, dtype=np.float64)

    def percentiles(self, x: int = 50):
        return np.percentile(self.asks, x), np.percentile(self.bids, x)

    def ptps(self):
        return np.ptp(self.asks), np.ptp(self.bids)

    def largest_volumes_prices(self) -> tuple[float, float]:
        return self.asks[self.asks[:, 1].argmax(), 0], self.bids[self.bids[:, 1].argmax(), 0]

    def volumes(self):
        return self.asks, self.bids

    def centroids(self) -> tuple[Any, Any]:
        return self.asks.mean(axis=0)[0], self.bids.mean(axis=0)[0]

    def get_accumulated_side(self, side):
        return list(zip(side[:, 0], np.cumsum(side[:, 1])))

    def get_accumulated_asks(self):
        return self.get_accumulated_side(self.asks)

    def get_accumulated_bids(self):
        return self.get_accumulated_side(self.bids)

    def get_max_ask(self):
        return max(self.get_accumulated_asks(), key=lambda x: x[1])

    def get_max_bids(self):
        return max(self.get_accumulated_bids(), key=lambda x: x[1])

    def get_balanced_prices(self):
        accumulated_asks = self.get_accumulated_asks()
        accumulated_asks_last = accumulated_asks[-1]
        accumulated_bids = self.get_accumulated_bids()
        accumulated_bids_last = accumulated_bids[-1]
        accumulated_asks_last_volume = accumulated_asks_last[1]
        accumulated_bids_last_volume = accumulated_bids_last[1]
        asks_bigger = accumulated_asks_last_volume > accumulated_bids_last_volume
        if asks_bigger:
            for aa in accumulated_asks:
                if aa[1] > accumulated_bids_last_volume:
                    return (aa[0], accumulated_bids_last[0])
        else:
            for ab in accumulated_bids:
                if ab[1] > accumulated_asks_last_volume:
                    return (accumulated_asks_last[0], ab[0])

    def get_absolute_center_price(self):
        min_ask = self.asks[0]
        max_bid = self.bids[0]
        return round((min_ask[0] + max_bid[0]) / 2.0, 1)

    def get_centroids_center_price(self):
        min_ask, max_bid = self.centroids()
        return round((min_ask + max_bid) / 2.0, 1)

    def get_all_means(self):
        (balanced_ask_price, balanced_bid_price) = self.get_balanced_prices()
        (asks_centroid, bids_centroid) = self.centroids()
        absolute_center = self.get_absolute_center_price()
        centroids_center = self.get_centroids_center_price()
        mean_center = round(float(np.mean([absolute_center, centroids_center])), 1)
        mean_max = round(float(np.mean([balanced_ask_price, asks_centroid])), 1)
        mean_min = round(float(np.mean([balanced_bid_price, bids_centroid])), 1)
        return mean_max, mean_center, mean_min

    def get_mark_price(self):
        return self.mark_price
