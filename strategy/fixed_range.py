from base.Settings import Settings
from data.enums import AmountSpacing, OrderType, PositionSide, Side
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
        price_sell_max_mult = file_input.price_sell_max_mult
        price_sell_min_mult = file_input.price_sell_min_mult
        price_buy_max_mult = file_input.price_buy_max_mult
        price_buy_min_mult = file_input.price_buy_min_mult
        mark_price = self.repo.get_mark_price(symbol=symbol).markPrice
        last_price = self.repo.get_ticker_price(symbol=symbol)
        position_risk = self.repo.get_position_risk(symbol=symbol)
        availableBalance = self.repo.get_account_info().availableBalance
        precision = 3
        order_quantity_min = 0.001
        order_quantity_max = 1000.0
        leverage = position_risk.leverage
        maxNotionalValue = position_risk.maxNotionalValue
        notional = position_risk.notional
        position_amount = position_risk.positionAmt
        current_buy_orders_num = len(self.repo.get_all_orders(symbol=symbol, side=Side.BUY))
        """ if position_amount == 0.0:
            if current_buy_orders_num != 0:
                self.repo.cancel_all_orders(symbol=symbol)
            self.repo.new_order(
                symbol=symbol,
                side=Side.BUY,
                quantity=0.03,
                position_side=PositionSide.LONG,
                order_type=OrderType.MARKET,
            )
            return
        else:
            self.repo.delete_all_side_orders(symbol=symbol, side=Side.SELL) """
        entry_price = mark_price if use_mark_price else position_risk.entryPrice
        center_price = entry_price if entry_price > 0.0 or use_mark_price else mark_price
        # center_price = mark_price + 100.0
        max_mm_position = (maxNotionalValue / 2.0) / last_price
        if abs(position_amount) >= abs(max_mm_position) and market_making:
            center_price = (
                min(entry_price, mark_price, last_price)
                if position_risk.positionSide == PositionSide.LONG
                else max(entry_price, mark_price, last_price)
            )
        fixed_range_grid = get_grid_maxs_and_mins(
            center_price=center_price,
            price_sell_max_mult=price_sell_max_mult,
            price_sell_min_mult=price_sell_min_mult,
            price_buy_max_mult=price_buy_max_mult,
            price_buy_min_mult=price_buy_min_mult,
        )
        # price_sell_max = 43000.0
        # price_sell_min = 42900.0
        # price_buy_max = 43050.0
        # price_buy_min = 42700.0
        buy_orders = []
        if abs(position_amount) < abs(max_mm_position) or not market_making:
            if position_amount == 0.0:
                buy_orders_num = 200
            buy_orders_quantities_and_prices = get_open_orders_quantities_and_prices(
                orders_num=buy_orders_num,
                high_price=fixed_range_grid.price_buy_max,
                low_price=fixed_range_grid.price_buy_min,
                available_balance=availableBalance,
                leverage=leverage,
                mark_price=mark_price,
                max_notional_value=maxNotionalValue,
                notional=notional,
                side=position_side,
                precision=precision,
                order_quantity_min=order_quantity_min,
                order_quantity_max=order_quantity_max,
                amount_spacing=AmountSpacing.GEOMETRIC,
                market_making=market_making,
                mm_buy_quantity=mm_buy_quantity,
            )
            side_open = Side.BUY if position_side == PositionSide.LONG else Side.SELL
            buy_orders = create_multiple_orders(
                symbol=symbol,
                side=side_open,
                quantities_and_prices=buy_orders_quantities_and_prices,
                position_side=position_side,
                time_in_force=time_in_force,
            )
        sell_orders_quantities_and_prices = get_close_orders_quantities_and_prices(
            orders_num=200 - len(buy_orders) if isinstance(buy_orders, list) else 0,
            high_price=fixed_range_grid.price_sell_max,
            low_price=fixed_range_grid.price_sell_min,
            amount=abs(position_amount),
            order_quantity_min=order_quantity_min,
            amount_spacing=AmountSpacing.GEOMETRIC,
            market_making=market_making,
            mm_sell_quantity=mm_sell_quantity,
        )
        side_close = Side.SELL if position_side == PositionSide.LONG else Side.BUY
        sell_orders = create_multiple_orders(
            symbol=symbol,
            side=side_close,
            quantities_and_prices=sell_orders_quantities_and_prices,
            position_side=position_side,
            time_in_force=time_in_force,
        )
        self.execute_orders(batched_orders=batched_lists(iterable=buy_orders + sell_orders, n=5))
