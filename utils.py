import datetime

import numpy as np

from enums import (
    TIF,
    OrderType,
    PositionSide,
    PriceMatch,
    PriceMatchNone,
    PriceMatchQueue,
    Side,
    TickerSymbol,
)


def create_order(
    symbol: TickerSymbol,
    side: Side,
    quantity: float,
    positionSide: PositionSide,
    price: float = 0.0,
    type: OrderType = OrderType.LIMIT,
    timeInForce: TIF = TIF.GTC,
    priceMatch: PriceMatch = PriceMatchNone.NONE,
):
    order = {
        "symbol": symbol,
        "side": side,
        "type": type,
        "quantity": quantity,
        "timeInForce": timeInForce,
        "positionSide": positionSide,
    }
    if priceMatch is PriceMatchNone.NONE:
        order["price"] = (price,)
    else:
        order["priceMatch"] = priceMatch
    return order


def create_all_queue_price_match_orders(
    symbol: TickerSymbol, side: Side, positionSide: PositionSide, quantity: float
):
    orders = []
    for name, member in PriceMatchQueue.__members__.items():
        if quantity > 0.0:
            orders.append(
                create_order(
                    symbol=symbol,
                    side=side,
                    quantity=quantity,
                    positionSide=positionSide,
                    priceMatch=member,
                )
            )
    return orders


def create_multiple_orders(
    symbol: TickerSymbol,
    side: Side,
    quantities_and_prices: list[tuple[float, float]],
    positionSide: PositionSide,
    type: OrderType = OrderType.LIMIT,
    timeInForce: TIF = TIF.GTC,
    priceMatch: PriceMatch = PriceMatchNone.NONE,
):
    result = []
    for i in quantities_and_prices:
        if priceMatch is PriceMatchNone.NONE:
            order = create_order(
                symbol=symbol,
                side=side,
                quantity=i[1],
                price=i[0],
                positionSide=positionSide,
                type=type,
                timeInForce=timeInForce,
            )
        else:
            order = create_order(
                symbol=symbol,
                side=side,
                quantity=i[1],
                price=i[0],
                positionSide=positionSide,
                type=type,
                timeInForce=timeInForce,
                priceMatch=priceMatch,
            )
        result.append(order)
    return result


def get_orders_quantities_and_prices(
    orders_num: int,
    high_price: float,
    low_price: float,
    amount: float,
):
    quantities_and_prices = []
    if amount > 0.0 and orders_num > 0:
        quantity = amount / orders_num
        opt_a = np.geomspace(start=low_price, stop=high_price, num=orders_num)
        opt_b = np.linspace(start=low_price, stop=high_price, num=orders_num)
        for i in opt_a:
            quantities_and_prices.append((round(i, 1), round(quantity, 3)))
    return quantities_and_prices


def print_date_and_time():
    print(f"date and time = {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
