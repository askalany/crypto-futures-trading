from rich import print
from data.enums import TickerSymbol

from repository.repository import TradeRepo
import numpy as np


def main():
    a = np.linspace(1,10,5)
    b = np.logspace(1,10,5)
    c = np.geomspace(1,10,5)
    print(f"{a=}")
    print(f"{b=}")
    print(f"{c=}")


if __name__ == "__main__":
    main()
