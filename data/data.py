from dataclasses import dataclass

from enums import (
    TIF,
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
    time_in_force: TIF = TIF.GTC
    price_match: PriceMatch = PriceMatchNone.NONE
