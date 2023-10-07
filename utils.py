import datetime
from typing import Any

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
) -> dict[str, Any]:
    order = {
        "symbol": symbol,
        "side": side,
        "type": type,
        "quantity": quantity,
        "timeInForce": timeInForce,
        "positionSide": positionSide,
    }
    if priceMatch is PriceMatchNone.NONE:
        order["price"] = price
    else:
        order["priceMatch"] = priceMatch
    return order


def create_all_queue_price_match_orders(
    symbol: TickerSymbol, side: Side, positionSide: PositionSide, quantity: float
) -> list[Any]:
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
) -> list[Any]:
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
    min_sell_amount: float = -1.0,
) -> list[Any]:
    quantities_and_prices = []
    if amount > 0.0 and orders_num > 0:
        order_amount = amount / orders_num
        quantity = order_amount if order_amount > min_sell_amount else min_sell_amount
        if order_amount > min_sell_amount:
            order_amount = min_sell_amount
            orders_num = int(amount / min_sell_amount)
        opt_a = np.geomspace(start=low_price, stop=high_price, num=orders_num)
        opt_b = np.linspace(start=low_price, stop=high_price, num=orders_num)
        for i in opt_a:
            quantities_and_prices.append((round(i, 1), round(quantity, 3)))
    return quantities_and_prices


def print_date_and_time() -> None:
    print(f"date and time = {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")


def get_scaled(volume_scale: float, num: int) -> tuple[list[float], float]:
    scaled: list[float] = [1]
    for i in range(0, num - 1):
        scaled.append(scaled[-1] * volume_scale)
    sum_scaled: float = float(sum(scaled))
    return scaled, sum_scaled


def get_scaled_mults(scaled: list[float], sum_scaled: float) -> list[float]:
    return list(map(lambda x: x / sum_scaled, scaled))


def make_it_smaller(
    total_amount: float, final_scaled: list[float]
) -> Any | list[float]:
    sum_final_scaled = sum(final_scaled)
    final_scaled[-1] = final_scaled[-1] - (sum_final_scaled - total_amount)
    if sum_final_scaled > total_amount:
        final_scaled = make_it_smaller(
            total_amount=total_amount, final_scaled=final_scaled
        )
    return final_scaled


def get_scaled_amounts(
    total_amount: float, volume_scale: float, num: int
) -> list[float]:
    scaled, sum_scaled = get_scaled(volume_scale=volume_scale, num=num)
    scaled_mults = get_scaled_mults(scaled=scaled, sum_scaled=sum_scaled)
    return make_it_smaller(
        total_amount=total_amount,
        final_scaled=list(map(lambda x: x * total_amount, scaled_mults)),
    )
