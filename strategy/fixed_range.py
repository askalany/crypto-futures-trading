from base.Settings import Settings
from data.enums import AmountSpacing, PositionSide, Side
from strategy.TradeStrategy import TradeStrategy
from utils.listutils import batched_lists
from utils.mathutils import get_grid_maxs_and_mins
from utils.orderutils import (
    create_multiple_orders,
    get_open_orders_quantities_and_prices,
    get_close_orders_quantities_and_prices,
)


class FixedRangeStrategy(TradeStrategy):
    def run_loop(self) -> None:
        file_input = Settings().file_input
        symbol = file_input.symbol
        position_side = file_input.position_side
        time_in_force = file_input.time_in_force
        use_mark_price = file_input.use_mark_price
        buy_orders_num = file_input.buy_orders_num
        sell_orders_num = file_input.sell_orders_num
        market_making = file_input.market_making
        mm_buy_quantity = file_input.mm_buy_quantity
        mm_sell_quantity = file_input.mm_sell_quantity
        price_sell_max_mult=file_input.price_sell_max_mult
        price_sell_min_mult=file_input.price_sell_min_mult
        price_buy_max_mult=file_input.price_buy_max_mult
        price_buy_min_mult=file_input.price_buy_min_mult
        mark_price = self.repo.get_mark_price(symbol).markPrice
        last_price = self.repo.get_ticker_price(symbol)
        position_risk = self.repo.get_position_risk(symbol=symbol)
        availableBalance = self.repo.get_account_info().availableBalance
        precision = 3
        order_quantity_min=0.001
        order_quantity_max=1000.0
        leverage = position_risk.leverage
        maxNotionalValue = position_risk.maxNotionalValue
        notional = position_risk.notional
        position_amount = position_risk.positionAmt
        entry_price = mark_price if use_mark_price else position_risk.entryPrice
        center_price = entry_price if entry_price > 0.0 or use_mark_price else mark_price
        # center_price = mark_price + 900.0#42200.0
        max_mm_position = (maxNotionalValue / 2.0) / last_price
        if abs(position_amount) >= abs(max_mm_position) and market_making:
            center_price = (
                min(entry_price, mark_price, last_price)
                if position_risk.positionSide == PositionSide.LONG
                else max(entry_price, mark_price, last_price)
            )
        (price_sell_max, price_sell_min, price_buy_max, price_buy_min) = get_grid_maxs_and_mins(
            center_price=center_price,
            price_sell_max_mult=price_sell_max_mult,
            price_sell_min_mult=price_sell_min_mult,
            price_buy_max_mult=price_buy_max_mult,
            price_buy_min_mult=price_buy_min_mult,
        )
        # price_sell_max = 42800.0
        # price_sell_min = 41500.0
        # price_buy_max = 41400.0
        # price_buy_min = 40800.0
        buy_orders = []
        if abs(position_amount) < abs(max_mm_position) or not market_making:
            buy_orders_quantities_and_prices = get_open_orders_quantities_and_prices(
                buy_orders_num,
                price_buy_max,
                price_buy_min,
                availableBalance,
                leverage,
                mark_price,
                maxNotionalValue,
                notional,
                position_side,
                precision,
                order_quantity_min,
                order_quantity_max,
                AmountSpacing.GEOMETRIC,
                market_making,
                mm_buy_quantity,
            )
            side_open = Side.BUY if position_side == PositionSide.LONG else Side.SELL
            buy_orders = create_multiple_orders(
                symbol,
                side_open,
                buy_orders_quantities_and_prices,
                position_side,
                time_in_force=time_in_force,
            )
        sell_orders_quantities_and_prices = get_close_orders_quantities_and_prices(
            200 - len(buy_orders) if isinstance(buy_orders, list) else 0,
            price_sell_max,
            price_sell_min,
            abs(position_amount),
            order_quantity_min,
            AmountSpacing.GEOMETRIC,
            market_making,
            mm_sell_quantity,
        )
        side_close = Side.SELL if position_side == PositionSide.LONG else Side.BUY
        sell_orders = create_multiple_orders(
            symbol,
            side_close,
            sell_orders_quantities_and_prices,
            position_side,
            time_in_force=time_in_force,
        )
        batched_orders = batched_lists(buy_orders + sell_orders, 5)
        self.execute_orders(batched_orders)
