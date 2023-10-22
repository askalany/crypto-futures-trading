from __future__ import annotations

from pydantic import BaseModel

from data.enums import PositionSide, Strategy, TickerSymbol, TimeInForce


class FileInput(BaseModel):
    once: bool
    use_mark_price: bool
    delay_seconds: float
    symbol: TickerSymbol
    strategy: Strategy
    position_side: PositionSide
    buy_orders_num: int = 100
    sell_orders_num: int = 100
    time_in_force: TimeInForce = TimeInForce.GTC
    price_sell_max_mult: float = 1.2
    price_sell_min_mult: float = 1.0008
    price_buy_max_mult: float = 0.9992
    price_buy_min_mult: float = 0.8
    market_making: bool = False
    mm_sell_quantity: float = 0.0
    mm_buy_quantity: float = 0.0
    leverage: int = 1
