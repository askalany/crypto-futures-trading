from dataclasses import dataclass

from enums import (
    TimeInForce,
    OrderType,
    PositionSide,
    PriceMatch,
    PriceMatchNone,
    Side,
    TickerSymbol,
)


@dataclass
class Order:
    symbol: TickerSymbol
    side: Side
    quantity: float
    position_snide: PositionSide
    price: float
    type: OrderType = OrderType.LIMIT
    time_in_force: TimeInForce = TimeInForce.GTC
    price_match: PriceMatch = PriceMatchNone.NONE
