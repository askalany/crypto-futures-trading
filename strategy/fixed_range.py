from data.enums import AmountSpacing, PositionSide, Side, TickerSymbol, TimeInForce
from strategy.TradeStrategy import TradeStrategy
from utils.listutils import batched_lists
from utils.mathutils import get_grid_maxs_and_mins
from utils.orderutils import create_multiple_orders, get_orders_quantities_and_prices

class FixedRangeStrategy(TradeStrategy):
    def __int__(
        self,
        symbol: TickerSymbol,
        position_side: PositionSide,
        buy_orders_num: int = 100,
        sell_orders_num: int = 100,
        use_mark_price: bool = False,
        time_in_force: TimeInForce = TimeInForce.GTC,
        price_sell_max_mult: float = 1.2,
        price_sell_min_mult: float = 1.0008,
        price_buy_max_mult: float = 0.9992,
        price_buy_min_mult: float = 0.8,
    ):
        super().__init__(
            symbol=symbol,
            position_side=position_side,
            buy_orders_num=buy_orders_num,
            sell_orders_num=sell_orders_num,
            use_mark_price=use_mark_price,
            time_in_force=time_in_force,
            price_sell_max_mult=price_sell_max_mult,
            price_sell_min_mult=price_sell_min_mult,
            price_buy_max_mult=price_buy_max_mult,
            price_buy_min_mult=price_buy_min_mult,
        )

    def run_loop(self):
        mark_price = self.repo.get_mark_price(symbol=self.symbol).markPrice
        position_risk = self.repo.get_position_risk(symbol=self.symbol)
        account_info = self.repo.get_account_info()
        entry_price = position_risk.entryPrice
        position_amount = position_risk.positionAmt
        entry_price = mark_price if self.use_mark_price else entry_price
        center_price = entry_price if entry_price > 0.0 else mark_price
        leveraged_balance = position_risk.leverage * min(account_info.availableBalance, position_risk.maxNotionalValue)
        amount_buy = leveraged_balance / center_price
        (
            price_sell_max,
            price_sell_min,
            price_buy_max,
            price_buy_min,
        ) = get_grid_maxs_and_mins(
            center_price=center_price,
            price_sell_max_mult=self.price_sell_max_mult,
            price_sell_min_mult=self.price_sell_min_mult,
            price_buy_max_mult=self.price_buy_max_mult,
            price_buy_min_mult=self.price_buy_min_mult,
        )
        buy_orders_quantities_and_prices = get_orders_quantities_and_prices(
            orders_num=self.buy_orders_num,
            high_price=price_buy_max,
            low_price=price_buy_min,
            amount=amount_buy,
            order_quantity_min=0.001,
            amount_spacing=AmountSpacing.GEOMETRIC,
        )
        buy_orders = create_multiple_orders(
            symbol=self.symbol,
            side=Side.BUY,
            quantities_and_prices=buy_orders_quantities_and_prices,
            position_side=self.position_side,
            time_in_force=self.time_in_force,
        )
        sell_orders_quantities_and_prices = get_orders_quantities_and_prices(
            orders_num=200 - len(buy_orders) if isinstance(buy_orders, list) else 0,
            high_price=price_sell_max,
            low_price=price_sell_min,
            amount=position_amount,
            order_quantity_min=0.001,
            amount_spacing=AmountSpacing.GEOMETRIC,
        )
        sell_orders = create_multiple_orders(
            symbol=self.symbol,
            side=Side.SELL,
            quantities_and_prices=sell_orders_quantities_and_prices,
            position_side=self.position_side,
            time_in_force=self.time_in_force,
        )
        batched_orders = batched_lists(buy_orders + sell_orders, 5)
        self.execute_orders(batched_orders)
