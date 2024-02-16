
from BinanceOrderBook import BinanceOrderBook

from repository.repository import TradeRepo
from rich import print


def main():
    print("try")
    repo = TradeRepo()
    binance_order_book = BinanceOrderBook(repo)
    largest_bid_price, largest_ask_price = binance_order_book.largest_volumes_prices()
    bids_centroid, asks_centroid = binance_order_book.centroids()
    bids_ptp, asks_ptp = binance_order_book.ptps()
    bids_percentile, asks_percentile = binance_order_book.percentiles()
    print(f"{bids_centroid=}, {asks_centroid=}")
    print(f"{largest_bid_price=}, {largest_ask_price=}")
    print(f"{bids_ptp=}, {asks_ptp=}")
    print(f"{bids_percentile=}, {asks_percentile=}")


if __name__ == "__main__":
    main()
