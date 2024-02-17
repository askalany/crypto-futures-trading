from BinanceOrderBook import BinanceOrderBook
from repository.repository import TradeRepo
from rich import print


def main():
    print("try")
    repo = TradeRepo()
    binance_order_book = BinanceOrderBook(repo, limit=50)
    max_asks = binance_order_book.get_max_ask()
    print(f"{max_asks=}")
    max_bids = binance_order_book.get_max_bids()
    print(f"{max_bids=}")


if __name__ == "__main__":
    main()
