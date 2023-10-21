from base.models.FileInput import FileInput
from data.enums import AmountSpacing, PositionSide, Side
from strategy.TradeStrategy import TradeStrategy
from utils.listutils import batched_lists
from utils.mathutils import get_grid_maxs_and_mins
from utils.orderutils import (
    create_multiple_orders,
    get_buy_orders_quantities_and_prices,
    get_sell_orders_quantities_and_prices,
)


class FixedRangeStrategy(TradeStrategy):
    def __int__(self, file_input: FileInput) -> None:
        super().__init__(file_input=file_input)

    def run_loop(self) -> None:
        mark_price = self.repo.get_mark_price(symbol=self.file_input.symbol).markPrice
        position_risk = self.repo.get_position_risk(symbol=self.file_input.symbol)
        account_info = self.repo.get_account_info()
        entry_price = position_risk.entryPrice
        position_amount = position_risk.positionAmt
        entry_price = mark_price if self.file_input.use_mark_price else entry_price
        center_price = entry_price if entry_price > 0.0 else mark_price
        max_mm_position = 2000.0
        if position_amount >= max_mm_position and self.file_input.market_making:
            center_price = min(position_risk.entryPrice, mark_price)
        (
            price_sell_max,
            price_sell_min,
            price_buy_max,
            price_buy_min,
        ) = get_grid_maxs_and_mins(
            center_price=center_price,
            price_sell_max_mult=self.file_input.price_sell_max_mult,
            price_sell_min_mult=self.file_input.price_sell_min_mult,
            price_buy_max_mult=self.file_input.price_buy_max_mult,
            price_buy_min_mult=self.file_input.price_buy_min_mult,
        )
        buy_orders = []
        if position_amount < max_mm_position or not self.file_input.market_making:
            buy_orders_quantities_and_prices = get_buy_orders_quantities_and_prices(
                orders_num=self.file_input.buy_orders_num,
                high_price=price_buy_max,
                low_price=price_buy_min,
                available_balance=account_info.availableBalance,
                leverage=position_risk.leverage,
                mark_price=mark_price,
                max_notional_value=position_risk.maxNotionalValue,
                notional=position_risk.notional,
                side=PositionSide.LONG,
                precision=3,
                order_quantity_min=0.001,
                order_quantity_max=1000.0,
                amount_spacing=AmountSpacing.GEOMETRIC,
                market_making=self.file_input.market_making,
                mm_buy_quantity=self.file_input.mm_buy_quantity,
            )
            buy_orders = create_multiple_orders(
                symbol=self.file_input.symbol,
                side=Side.BUY,
                quantities_and_prices=buy_orders_quantities_and_prices,
                position_side=self.file_input.position_side,
                time_in_force=self.file_input.time_in_force,
            )
        sell_orders_quantities_and_prices = get_sell_orders_quantities_and_prices(
            orders_num=200 - len(buy_orders) if isinstance(buy_orders, list) else 0,
            high_price=price_sell_max,
            low_price=price_sell_min,
            amount=position_amount,
            order_quantity_min=0.001,
            amount_spacing=AmountSpacing.GEOMETRIC,
            market_making=self.file_input.market_making,
            mm_sell_quantity=self.file_input.mm_sell_quantity,
        )
        sell_orders = create_multiple_orders(
            symbol=self.file_input.symbol,
            side=Side.SELL,
            quantities_and_prices=sell_orders_quantities_and_prices,
            position_side=self.file_input.position_side,
            time_in_force=self.file_input.time_in_force,
        )
        batched_orders = batched_lists(buy_orders + sell_orders, 5)
        self.execute_orders(batched_orders)
