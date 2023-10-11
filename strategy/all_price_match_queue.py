# pylint: disable=missing-docstring

from data.enums import PositionSide, Side, TickerSymbol, TIF
from strategy.TradeStrategy import TradeStrategy
from utils.utils import (
    create_all_queue_price_match_orders,
    get_max_buy_amount,
)


class AllPriceMatchQueueStrategy(TradeStrategy):
    def __int__(
        self,
        symbol: TickerSymbol,
        position_side: PositionSide,
        tif: TIF = TIF.GTC,
    ):
        super().__init__(
            self,
            symbol=symbol,
            position_side=position_side,
            buy_orders_num=4,
            sell_orders_num=4,
            tif=tif,
        )

    def run_loop(self):
        mark_price = self.repo.get_mark_price(symbol=self.symbol)
        position_amount = self.repo.get_hedge_position_amount(symbol=self.symbol)
        leverage = self.repo.get_leverage(symbol=self.symbol)
        available_balance = self.repo.get_available_balance()
        buy_amount = get_max_buy_amount(
            leverage=leverage,
            available_balance=available_balance,
            mark_price=mark_price,
        )
        buy_order_amount = round(buy_amount / float(self.buy_orders_num), 4)
        sell_order_amount = round(position_amount / float(self.sell_orders_num), 4)
        buy_orders = create_all_queue_price_match_orders(
            symbol=self.symbol,
            side=Side.BUY,
            position_side=self.position_side,
            quantity=min(buy_order_amount, 1000.0),
        )
        sell_orders = create_all_queue_price_match_orders(
            symbol=self.symbol,
            side=Side.SELL,
            position_side=self.position_side,
            quantity=min(sell_order_amount, 1000.0),
        )
        self.execute_orders(buy_orders + sell_orders)