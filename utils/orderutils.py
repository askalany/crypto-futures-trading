from typing import Any
from functools import cache
from data.enums import (
    AmountSpacing,
    OrderType,
    PositionSide,
    PriceMatch,
    PriceMatchNone,
    PriceMatchOpponent,
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
    if price < 0.0:
        raise ValueError("Price cannot be negative")
    if order_type in [OrderType.LIMIT, OrderType.MARKET, OrderType.STOP, OrderType.TAKE_PROFIT] and quantity < 0.0:
        raise ValueError("Price cannot be negative")
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
    members = (
        PriceMatchQueue.__members__.items()
        if (position_side == PositionSide.LONG and side == Side.BUY)
        or (position_side == PositionSide.SHORT and side == Side.SELL)
        else PriceMatchOpponent.__members__.items()
    )
    for name, member in members:
        if quantity > 0.0:
            order = create_order(
                symbol=symbol, side=side, quantity=quantity, position_side=position_side, price_match=member
            )
            orders.append(order)
    return orders


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


@cache
def get_orders(min_order, multiplier, orders_num):
    orders = [min_order]
    [orders.append(round(multiplier * orders[i - 1], 3)) for i in range(1, orders_num)]
    return orders


def get_optimized_orders(total, orders_num, min_order):
    multiplier = 1.0
    while True:
        multiplier = round(multiplier + (1 / 1000.0), 3)
        orders = get_orders(min_order, multiplier, orders_num)
        if sum(orders) > total:
            multiplier = round(multiplier - (1 / 1000.0), 3)
            orders = get_orders(min_order, multiplier, orders_num)
            return orders


def get_open_orders_quantities_and_prices(
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
    optimized_orders = get_optimized_orders(available_balance, orders_num, 200.0)
    quantities_and_prices = []
    prices.sort(reverse=True)
    for i, o in zip(prices, optimized_orders):
        order_price = round(i, 1)
        max_quantity = max_open_quantity(
            leverage=leverage,
            available_balance=o,
            order_price=order_price,
            mark_price=mark_price,
            max_notional_value=max_notional_value,
            notional=notional,
            side=side,
            precision=precision,
        )
        order_quantity = min(mm_buy_quantity, max_quantity) if market_making else max_quantity
        order_quantity = min(order_quantity, order_quantity_max)
        order_quantity = max(order_quantity, order_quantity_min)
        quantities_and_prices.append((order_price, round(order_quantity, precision)))
    return quantities_and_prices


def get_close_orders_quantities_and_prices(
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
        min(mm_sell_quantity, (amount / orders_num)) if market_making else (amount / orders_num), order_quantity_min
    )
    if not market_making:
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
    return round(min(leveraged_balance / leveraged_gap, remaining_notional / order_price), precision)


def get_prices_list(orders_num: int, high_price: float, low_price: float, amount_spacing: AmountSpacing) -> list[float]:
    return (
        get_linear_scale(orders_num=orders_num, high_price=high_price, low_price=low_price)
        if amount_spacing is AmountSpacing.LINEAR
        else get_geom_scale(orders_num=orders_num, high_price=high_price, low_price=low_price)
    )
