from data.enums import TickerSymbol
from repository.repository import TradeRepo
from rich import print


def main():
    repo = TradeRepo()
    print(f"{repo.get_account_info().availableBalance}")


if __name__ == "__main__":
    main()
