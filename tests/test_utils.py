from enums import (
    TIF,
    OrderType,
    PositionSide,
    PriceMatchNone,
    PriceMatchQueue,
    Side,
    TickerSymbol,
)
from utils import create_order


def order_value():
    symbol = TickerSymbol.BTCUSDT
    side = Side.BUY
    quantity = 1.0
    price = 1.0
    positionSide = PositionSide.LONG
    type = OrderType.LIMIT
    timeInForce = TIF.GTC
    priceMatch = PriceMatchNone.NONE
    return symbol, side, quantity, price, positionSide, type, timeInForce, priceMatch


def test_create_order_price():
    (
        symbol,
        side,
        quantity,
        price,
        positionSide,
        type,
        timeInForce,
        priceMatch,
    ) = order_value()
    order = create_order(
        symbol=symbol,
        side=side,
        quantity=quantity,
        price=price,
        positionSide=positionSide,
        type=type,
        timeInForce=timeInForce,
        priceMatch=priceMatch,
    )
    assert "price" in order


def test_create_order_price_value():
    (
        symbol,
        side,
        quantity,
        price,
        positionSide,
        type,
        timeInForce,
        priceMatch,
    ) = order_value()
    order = create_order(
        symbol=symbol,
        side=side,
        quantity=quantity,
        price=price,
        positionSide=positionSide,
        type=type,
        timeInForce=timeInForce,
        priceMatch=priceMatch,
    )
    assert order["price"] == price


def test_create_order_price_match():
    (
        symbol,
        side,
        quantity,
        price,
        positionSide,
        type,
        timeInForce,
        priceMatch,
    ) = order_value()
    order = create_order(
        symbol=symbol,
        side=side,
        quantity=quantity,
        price=price,
        positionSide=positionSide,
        type=type,
        timeInForce=timeInForce,
        priceMatch=PriceMatchQueue.QUEUE,
    )
    assert "priceMatch" in order
