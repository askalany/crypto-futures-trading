from typing import Any

from data.enums import (
    AmountSpacing,
    OrderType,
    PositionSide,
    PriceMatch,
    PriceMatchNone,
    PriceMatchQueue,
    Side,
    TickerSymbol,
    TimeInForce,
)
from utils.mathutils import get_geom_scale, get_linear_scale


def create_order(
    symbol: TickerSymbol,
    side: Side,
    quantity: float,
    position_side: PositionSide,
    price: float = 0.0,
    order_type: OrderType = OrderType.LIMIT,
    time_in_force: TimeInForce = TimeInForce.GTC,
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
    time_in_force: TimeInForce = TimeInForce.GTC,
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


def get_buy_orders_quantities_and_prices(
    orders_num: int,
    high_price: float,
    low_price: float,
    available_balance: float,
    leverage: int,
    mark_price: float,
    max_notional_value: float,
    notional: float,
    side: PositionSide,
    precision: int,
    order_quantity_min: float,
    order_quantity_max: float,
    amount_spacing: AmountSpacing = AmountSpacing.LINEAR,
    market_making: bool = False,
    mm_buy_quantity: float = 0.0,
) -> list[tuple[float, float]]:
    if orders_num == 0:
        return []
    prices = get_prices_list(orders_num, high_price, low_price, amount_spacing)
    order_dollar_amount = available_balance / orders_num
    quantities_and_prices = []
    for i in prices:
        order_price = round(i, 1)
        max_quantity = max_open_quantity(
            leverage=leverage,
            available_balance=order_dollar_amount,
            order_price=order_price,
            mark_price=mark_price,
            max_notional_value=max_notional_value,
            notional=notional,
            side=side,
            precision=precision,
        )
        order_quantity = (
            min(mm_buy_quantity, max_quantity) if market_making else max_quantity
        )
        order_quantity = min(order_quantity, order_quantity_max)
        order_quantity = max(order_quantity, order_quantity_min)
        quantities_and_prices.append((order_price, round(order_quantity, precision)))
    return quantities_and_prices


def get_sell_orders_quantities_and_prices(
    orders_num: int,
    high_price: float,
    low_price: float,
    amount: float,
    order_quantity_min: float = -1.0,
    amount_spacing: AmountSpacing = AmountSpacing.LINEAR,
    market_making: bool = False,
    mm_sell_quantity: float = 0.0,
) -> list[tuple[float, float]]:
    if orders_num < 0:
        raise ValueError("orders_num must be positive")
    if amount < 0.0:
        raise ValueError("amount must be positive")
    if orders_num == 0 or amount < order_quantity_min:
        return []
    order_amount = max(
        max(mm_sell_quantity, (amount / orders_num))
        if market_making
        else (amount / orders_num),
        order_quantity_min,
    )
    orders_num = int(amount / order_amount)
    prices = get_prices_list(orders_num, high_price, low_price, amount_spacing)
    return [(round(i, 1), round(order_amount, 3)) for i in prices]


def max_open_quantity(
    leverage: int,
    available_balance: float,
    order_price: float,
    mark_price: float,
    max_notional_value: float,
    notional: float,
    side: PositionSide,
    precision: int,
) -> float:
    sign = 1.0 if side == PositionSide.LONG else -1.0
    leveraged_balance = float(leverage) * available_balance
    leveraged_order_mark_diff = sign * leverage * (order_price - mark_price)
    c = 0.0
    if order_price < mark_price:
        c = min(order_price, mark_price)
    else:
        c = max(order_price, mark_price)
    leveraged_gap = c + max(leveraged_order_mark_diff, 0)
    remaining_notional = max_notional_value - notional
    return round(
        min(leveraged_balance / leveraged_gap, remaining_notional / order_price),
        precision,
    )


def get_prices_list(
    orders_num: int, high_price: float, low_price: float, amount_spacing: AmountSpacing
) -> list[float]:
    return (
        get_linear_scale(
            orders_num=orders_num, high_price=high_price, low_price=low_price
        )
        if amount_spacing is AmountSpacing.LINEAR
        else get_geom_scale(
            orders_num=orders_num, high_price=high_price, low_price=low_price
        )
    )
