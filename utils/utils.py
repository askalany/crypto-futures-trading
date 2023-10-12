# pylint: disable=missing-docstring
import datetime
import json
from itertools import islice
from typing import Any

import numpy as np

# pylint: disable=redefined-builtin
from rich import print

from base.helpers import get_enum_member_from_name
from data.enums import (
    ALL_ENUMS,
    TIF,
    AmountSpacing,
    OrderType,
    PositionSide,
    PriceMatch,
    PriceMatchNone,
    PriceMatchQueue,
    Side,
    Strategy,
    TickerSymbol,
)


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


def get_geom_scale(orders_num: int, high_price: float, low_price: float):
    return np.geomspace(start=low_price, stop=high_price, num=orders_num)


def get_linear_scale(orders_num: int, high_price: float, low_price: float):
    return np.linspace(start=low_price, stop=high_price, num=orders_num)


def print_date_and_time() -> None:
    print(get_date_and_time())


def get_date_and_time():
    return f"date and time = {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"


def get_scaled(volume_scale: float, num: int) -> tuple[list[float], float]:
    if volume_scale <= 0.0:
        raise ValueError("volume_scale must be greater than 0.0")
    if num <= 0:
        raise ValueError("num must be greater than 0")
    scaled: list[float] = [1]
    scaled.extend(scaled[-1] * volume_scale for _ in range(num - 1))
    sum_scaled: float = float(sum(scaled))
    return scaled, sum_scaled


def get_scaled_mults(scaled: list[float], sum_scaled: float) -> list[float]:
    if not scaled:
        return []
    if sum_scaled < 0.0:
        raise ValueError("sum_scaled must be greater than 0.0")
    if sum_scaled == 0.0:
        raise ZeroDivisionError("sum_scaled must be greater than 0.0")
    return [x / sum_scaled for x in scaled]


def make_it_smaller(
    total_amount: float, final_scaled: list[float]
) -> Any | list[float]:
    while sum(final_scaled) > total_amount:
        final_scaled[-1] -= sum(final_scaled) - total_amount
    return final_scaled


def get_scaled_amounts(
    total_amount: float, volume_scale: float, num: int
) -> list[float]:
    return make_it_smaller(
        total_amount,
        [x * total_amount for x in get_scaled_mults(*get_scaled(volume_scale, num))],
    )


def batched(iterable, n):
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


def batched_lists(iterable, n) -> list[list[Any]]:
    b = batched(iterable=iterable, n=n)
    return [list(i) for i in b]


def check_grid_maxs_and_mins(
    price_sell_max, price_sell_min, price_buy_max, price_buy_min
) -> None:
    if not (price_buy_min < price_buy_max < price_sell_min < price_sell_max):
        raise ValueError(
            f"{price_sell_max=}, {price_sell_min=}, {price_buy_max=}, {price_buy_min=} Invalid price ranges"
        )


def get_grid_maxs_and_mins(
    center_price: float,
    price_sell_max_mult: float,
    price_sell_min_mult: float,
    price_buy_max_mult: float,
    price_buy_min_mult: float,
) -> tuple[float, float, float, float]:
    price_sell_max = center_price * price_sell_max_mult
    price_sell_min = center_price * price_sell_min_mult
    price_buy_max = center_price * price_buy_max_mult
    price_buy_min = center_price * price_buy_min_mult
    check_grid_maxs_and_mins(
        price_sell_max=price_sell_max,
        price_sell_min=price_sell_min,
        price_buy_max=price_buy_max,
        price_buy_min=price_buy_min,
    )
    return price_sell_max, price_sell_min, price_buy_max, price_buy_min


def get_max_buy_amount(
    leverage: int, available_balance: float, mark_price: float
) -> float:
    if leverage <= 0 or available_balance < 0 or mark_price <= 0.0:
        raise ValueError("Invalid input values")
    return (leverage * available_balance) / mark_price


def check_file_inputs(
    once: bool,
    use_mark_price: bool,
    delay_seconds: float,
    symbol: Any,
    strategy: Any,
    position_side: Any,
    buy_orders_num: int,
    sell_orders_num: int,
    tif: Any,
) -> tuple[bool, bool, float, TickerSymbol, Strategy, PositionSide, int, int, TIF]:
    if not isinstance(symbol, TickerSymbol):
        raise ValueError("incorrect input for symbol")
    if not isinstance(strategy, Strategy):
        raise ValueError("incorrect input for strategy")
    if not isinstance(position_side, PositionSide):
        raise ValueError("incorrect input for position_side")
    if not isinstance(tif, TIF):
        raise ValueError("incorrect input for tif")
    return (
        once,
        use_mark_price,
        delay_seconds,
        symbol,
        strategy,
        position_side,
        buy_orders_num,
        sell_orders_num,
        tif,
    )


def get_inputs_from_file(
    file_name: str = "my_trading.json",
) -> tuple[
    bool,
    bool,
    float,
    TickerSymbol,
    Strategy,
    PositionSide,
    int,
    int,
    TIF,
    float,
    float,
    float,
    float,
]:
    f = open(file_name, "r")
    read = f.read()
    data = json.loads(read)
    once_input = data["once"]
    use_mark_price_input = data["use_mark_price"]
    delay_seconds_input = data["delay_seconds"]
    symbol_input = get_enum_member_from_name(data["symbol"], ALL_ENUMS)
    strategy_input = get_enum_member_from_name(data["strategy"], ALL_ENUMS)
    position_side_input = get_enum_member_from_name(data["position_side"], ALL_ENUMS)
    buy_orders_num_input = data["buy_orders_num"]
    sell_orders_num_input = data["sell_orders_num"]
    tif_input = get_enum_member_from_name(data["tif"], ALL_ENUMS)
    price_sell_max_mult: float = data["price_sell_max_mult"]
    price_sell_min_mult: float = data["price_sell_min_mult"]
    price_buy_max_mult: float = data["price_buy_max_mult"]
    price_buy_min_mult: float = data["price_buy_min_mult"]
    if not isinstance(symbol_input, TickerSymbol):
        raise ValueError("incorrect input for symbol")
    if not isinstance(strategy_input, Strategy):
        raise ValueError("incorrect input for strategy")
    if not isinstance(position_side_input, PositionSide):
        raise ValueError("incorrect input for position_side")
    if not isinstance(tif_input, TIF):
        raise ValueError("incorrect input for tif")
    return (
        once_input,
        use_mark_price_input,
        delay_seconds_input,
        symbol_input,
        strategy_input,
        position_side_input,
        buy_orders_num_input,
        sell_orders_num_input,
        tif_input,
        price_sell_max_mult,
        price_sell_min_mult,
        price_buy_max_mult,
        price_buy_min_mult,
    )
