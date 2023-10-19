from data.enums import PositionSide, Side, TickerSymbol, TimeInForce
from strategy.TradeStrategy import TradeStrategy
from utils.mathutils import get_max_buy_amount
from utils.orderutils import create_all_queue_price_match_orders


class AllPriceMatchQueueStrategy(TradeStrategy):
    def __int__(
        self,
        symbol: TickerSymbol,
        position_side: PositionSide,
        time_in_force: TimeInForce = TimeInForce.GTC,
    ):
        super().__init__(
            symbol=symbol,
            position_side=position_side,
            buy_orders_num=4,
            sell_orders_num=4,
            time_in_force=time_in_force,
        )

    def run_loop(self):
        self.repo.cancel_all_orders(symbol=self.symbol)
        mark_price = self.repo.get_mark_price(symbol=self.symbol).markPrice
        position_risk = self.repo.get_position_risk(symbol=self.symbol)
        account_info = self.repo.get_account_info()
        buy_amount = get_max_buy_amount(
            leverage=position_risk.leverage,
            available_balance=account_info.availableBalance,
            mark_price=mark_price,
        )
        buy_order_amount = round(buy_amount / float(self.buy_orders_num), 4)
        sell_order_amount = round(
            position_risk.positionAmt / float(self.sell_orders_num), 4
        )
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
