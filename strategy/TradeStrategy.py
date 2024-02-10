import concurrent.futures
from typing import Any

from repository.repository import TradeRepo


class TradeStrategy:
    def __init__(self, repo: TradeRepo = TradeRepo()) -> None:
        self.repo = repo

    def work(self, order) -> Any | dict[Any, Any]:
        if isinstance(order, list):
            return self.repo.new_batch_order(orders=order)
        if "priceMatch" in order:
            response = self.repo.new_order(
                symbol=order["symbol"],
                side=order["side"],
                quantity=order["quantity"],
                position_side=order["positionSide"],
                price_match=order["priceMatch"],
            )

        else:
            response = self.repo.new_order(
                symbol=order["symbol"],
                side=order["side"],
                quantity=order["quantity"],
                position_side=order["positionSide"],
                price=order["price"],
            )
        return response

    def execute_orders(self, batched_orders) -> None:
        for order in batched_orders:
            self.work(order)
        #with concurrent.futures.ThreadPoolExecutor(max_workers=61) as executor:
            #executor.map(self.work, batched_orders, chunksize=5)

    def run_loop(self) -> None:
        pass
