import datetime
from math import floor
from typing import Any

import numpy as np
from rich import print

from enums import (TIF, AmountSpacing, OrderType, PositionSide, PriceMatch,
                   PriceMatchNone, PriceMatchQueue, Side, TickerSymbol)


def create_order(
    symbol: TickerSymbol,
    side: Side,
    quantity: float,
    position_side: PositionSide,
    price: float = 0.0,
    order_type: OrderType = OrderType.LIMIT,
    time_in_force: TIF = TIF.GTC,
    price_match: PriceMatch = PriceMatchNone.NONE,
) -> dict[str, Any]:
    order = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
        "timeInForce": time_in_force,
        "positionSide": position_side,
    }
    if price_match is PriceMatchNone.NONE:
        order["price"] = price
    else:
        order["priceMatch"] = price_match
    return order


def create_all_queue_price_match_orders(
    symbol: TickerSymbol, side: Side, position_side: PositionSide, quantity: float
) -> list[Any]:
    orders = []
    for name, member in PriceMatchQueue.__members__.items():
        if quantity > 0.0:
            orders.append(
                create_order(
                    symbol=symbol,
                    side=side,
                    quantity=quantity,
                    position_side=position_side,
                    price_match=member,
                )
            )
    return orders


def create_multiple_orders(
    symbol: TickerSymbol,
    side: Side,
    quantities_and_prices: list[tuple[float, float]],
    position_side: PositionSide,
    order_type: OrderType = OrderType.LIMIT,
    time_in_force: TIF = TIF.GTC,
    price_match: PriceMatch = PriceMatchNone.NONE,
) -> list[Any]:
    result = []
    for i in quantities_and_prices:
        if price_match is PriceMatchNone.NONE:
            order = create_order(
                symbol=symbol,
                side=side,
                quantity=i[1],
                price=i[0],
                position_side=position_side,
                order_type=order_type,
                time_in_force=time_in_force,
            )
        else:
            order = create_order(
                symbol=symbol,
                side=side,
                quantity=i[1],
                price=i[0],
                position_side=position_side,
                order_type=order_type,
                time_in_force=time_in_force,
                price_match=price_match,
            )
        result.append(order)
    return result


def get_orders_quantities_and_prices(
    orders_num: int,
    high_price: float,
    low_price: float,
    amount: float,
    order_quantity_min: float = -1.0,
    amount_spacing: AmountSpacing = AmountSpacing.LINEAR,
) -> list[Any]:
    quantities_and_prices = []
    if amount > 0.0 and orders_num > 0:
        order_amount = amount / orders_num
        quantity = (
            order_amount if order_amount > order_quantity_min else order_quantity_min
        )
        if order_amount < order_quantity_min:
            quantity = order_quantity_min
            orders_num = int(amount / order_quantity_min)
        amount_spacing_list = (
            np.linspace(start=low_price, stop=high_price, num=orders_num)
            if amount_spacing is AmountSpacing.LINEAR
            else np.geomspace(start=low_price, stop=high_price, num=orders_num)
        )
        quantities_and_prices = [
            (round(i, 1), round(quantity, 3)) for i in amount_spacing_list
        ]
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
    final_scaled[-1] -= sum_final_scaled - total_amount
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

def split_into_num(num: int, length: int):
    multiples = floor(length / num)
    remainder = length % 5
    return multiples, remainder