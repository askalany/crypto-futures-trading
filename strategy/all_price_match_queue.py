from data.enums import Side
from strategy.TradeStrategy import TradeStrategy
from utils.mathutils import get_max_buy_amount
from utils.orderutils import create_all_queue_price_match_orders
from base.Settings import Settings

class AllPriceMatchQueueStrategy(TradeStrategy):
    def run_loop(self):
        file_input = Settings().file_input
        symbol = Settings().file_input.symbol
        self.repo.cancel_all_orders(symbol)
        position_side= file_input.position_side
        mark_price = self.repo.get_mark_price(symbol=symbol).markPrice
        position_risk = self.repo.get_position_risk(symbol=symbol)
        account_info = self.repo.get_account_info()
        buy_amount = get_max_buy_amount(
            leverage=position_risk.leverage, available_balance=account_info.availableBalance, mark_price=mark_price
        )
        buy_order_amount = round(buy_amount / float(file_input.buy_orders_num), 4)
        sell_order_amount = round(position_risk.positionAmt / float(file_input.sell_orders_num), 4)
        buy_orders = create_all_queue_price_match_orders(
            symbol=file_input.symbol,
            side=Side.BUY,
            position_side=position_side,
            quantity=min(buy_order_amount, 1000.0),
        )
        sell_orders = create_all_queue_price_match_orders(
            symbol=symbol,
            side=Side.SELL,
            position_side=position_side,
            quantity=min(sell_order_amount, 1000.0),
        )
        self.execute_orders(buy_orders + sell_orders)
