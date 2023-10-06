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
    positionSide: PositionSide
    price: float
    type: OrderType = OrderType.LIMIT
    timeInForce: TIF = TIF.GTC
    priceMatch: PriceMatch = PriceMatchNone.NONE
