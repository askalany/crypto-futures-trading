from dataclasses import dataclass
from enums import TIF, OrderType, PositionSide, PriceMatch, Side, TickerSymbol


@dataclass
class Order:
    symbol: TickerSymbol
    side: Side
    quantity: float
    positionSide: PositionSide
    price: float
    type: OrderType
    timeInForce = TIF.GTC
    priceMatch: PriceMatch
