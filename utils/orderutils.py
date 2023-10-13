from typing import Any

from data.enums import (
    TIF,
    AmountSpacing,
    OrderType,
    PositionSide,
    PriceMatch,
    PriceMatchNone,
    PriceMatchQueue,
    Side,
    TickerSymbol,
)
from utils.mathutils import get_geom_scale, get_linear_scale


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
    return [
        create_order(
            symbol=symbol,
            side=side,
            quantity=quantity,
            position_side=position_side,
            price_match=member,
        )
        for name, member in PriceMatchQueue.__members__.items()
        if quantity > 0.0
    ]


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
        quantity = max(order_amount, order_quantity_min)
        if order_amount < order_quantity_min:
            quantity = order_quantity_min
            orders_num = int(amount / order_quantity_min)
        amount_spacing_list = (
            get_linear_scale(
                orders_num=orders_num, high_price=high_price, low_price=low_price
            )
            if amount_spacing is AmountSpacing.LINEAR
            else get_geom_scale(
                orders_num=orders_num, high_price=high_price, low_price=low_price
            )
        )
        quantities_and_prices = [
            (round(i, 1), round(quantity, 3)) for i in amount_spacing_list
        ]
    return quantities_and_prices
