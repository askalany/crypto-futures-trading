import concurrent.futures
from typing import Any

from data.enums import PositionSide, TickerSymbol, TIF
from repository.repository import TradeRepo


class TradeStrategy:
    def __init__(
        self,
        symbol: TickerSymbol,
        position_side: PositionSide,
        repo: TradeRepo = TradeRepo(),
        buy_orders_num: int = 100,
        sell_orders_num: int = 100,
        use_mark_price: bool = False,
        tif: TIF = TIF.GTC,
    ):
        self.symbol = symbol
        self.position_side = position_side
        self.repo = repo
        self.buy_orders_num = buy_orders_num
        self.sell_orders_num = sell_orders_num
        self.use_mark_price = use_mark_price
        self.tif = tif

    def work(self, order) -> Any | dict[Any, Any]:
        if isinstance(order, list):
            return self.repo.new_batch_order(orders=order)
        if "priceMatch" in order:
            return self.repo.new_order(
                symbol=order["symbol"],
                side=order["side"],
                quantity=order["quantity"],
                position_side=order["positionSide"],
                price_match=order["priceMatch"],
            )
        else:
            return self.repo.new_order(
                symbol=order["symbol"],
                side=order["side"],
                quantity=order["quantity"],
                position_side=order["positionSide"],
                price=order["price"],
            )

    def execute_orders(self, batched_orders):
        with concurrent.futures.ProcessPoolExecutor(max_workers=61) as executor:
            executor.map(self.work, batched_orders, chunksize=5)

    def run_loop(self):
        pass