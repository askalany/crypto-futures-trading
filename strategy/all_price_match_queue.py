from data.enums import TIF, PositionSide, Side, TickerSymbol
from strategy.TradeStrategy import TradeStrategy
from utils.mathutils import get_max_buy_amount
from utils.orderutils import create_all_queue_price_match_orders


class AllPriceMatchQueueStrategy(TradeStrategy):
    def __int__(
        self,
        symbol: TickerSymbol,
        position_side: PositionSide,
        tif: TIF = TIF.GTC,
    ):
        super().__init__(
            symbol=symbol,
            position_side=position_side,
            buy_orders_num=4,
            sell_orders_num=4,
            tif=tif,
        )

    def run_loop(self):
        self.repo.cancel_all_orders(symbol=self.symbol)
        mark_price = float(self.repo.get_mark_price(symbol=self.symbol).markPrice)
        position_amount = float(self.repo.get_position_risk(symbol=self.symbol).positionAmt)
        leverage = int(self.repo.get_position_risk(symbol=self.symbol).leverage)
        available_balance = float(self.repo.get_account_info().availableBalance)
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
