from typing import List, Tuple

import numpy as np
from base.models.FixedRangeGrid import FixedRangeGrid

from data.enums import PositionSide


def get_geom_scale(orders_num: int, high_price: float, low_price: float) -> List[float]:
    return np.geomspace(start=low_price, stop=high_price, num=orders_num, dtype=np.float64).tolist()


def get_linear_scale(orders_num: int, high_price: float, low_price: float) -> List[float]:
    return np.linspace(start=low_price, stop=high_price, num=orders_num, dtype=np.float64).tolist()


def get_scaled(volume_scale: float, num: int) -> Tuple[List[float], float]:
    if volume_scale <= 0.0 or num <= 0:
        raise ValueError("volume_scale and num must be greater than 0")

    scaled: List[float] = [1.0]
    factor = volume_scale
    for _ in range(num - 1):
        scaled.append(scaled[-1] * factor)

    sum_scaled: float = sum(scaled)
    return scaled, sum_scaled


def get_scaled_mults(scaled: List[float], sum_scaled: float) -> List[float]:
    if sum_scaled <= 0.0:
        raise ValueError("sum_scaled must be greater than 0.0")

    return [x / sum_scaled for x in scaled]


def make_it_smaller(total_amount: float, final_scaled: List[float]) -> List[float]:
    while sum(final_scaled) > total_amount:
        final_scaled[-1] -= sum(final_scaled) - total_amount
    return final_scaled


def get_scaled_amounts(total_amount: float, volume_scale: float, num: int) -> List[float]:
    scaled, sum_scaled = get_scaled(volume_scale, num)
    scaled_mults = get_scaled_mults(scaled, sum_scaled)
    return make_it_smaller(total_amount, [x * total_amount for x in scaled_mults])


def check_grid_maxs_and_mins(price_sell_max, price_sell_min, price_buy_max, price_buy_min) -> None:
    if not (price_buy_min < price_buy_max < price_sell_min < price_sell_max):
        raise ValueError(
            f"Invalid price ranges: {price_sell_max=}, {price_sell_min=}, {price_buy_max=}, {price_buy_min=}"
        )


def get_grid_maxs_and_mins(
    center_price: float,
    price_sell_max_mult: float,
    price_sell_min_mult: float,
    price_buy_max_mult: float,
    price_buy_min_mult: float,
) -> FixedRangeGrid:
    price_sell_max, price_sell_min, price_buy_max, price_buy_min = (
        center_price * price_sell_max_mult,
        center_price * price_sell_min_mult,
        center_price * price_buy_max_mult,
        center_price * price_buy_min_mult,
    )
    check_grid_maxs_and_mins(
        price_sell_max=price_sell_max,
        price_sell_min=price_sell_min,
        price_buy_max=price_buy_max,
        price_buy_min=price_buy_min,
    )
    return FixedRangeGrid(
        price_sell_max=price_sell_max,
        price_sell_min=price_sell_min,
        price_buy_max=price_buy_max,
        price_buy_min=price_buy_min,
    )


def get_max_buy_amount(leverage: int, available_balance: float, mark_price: float) -> float:
    if leverage <= 0 or available_balance < 0 or mark_price <= 0.0:
        raise ValueError("Invalid input values")

    return (leverage * available_balance) / mark_price


def cost_to_open_position(
    quantity: float,
    leverage: int,
    side: PositionSide,
    mark_price: float,
    order_price: float,
    precision: int,
    number_of_Contract: int = 1,
) -> float:
    # Step 1: Calculate the Initial Margin
    notional_value = order_price * quantity
    initial_margin = notional_value / leverage

    # Step 2: Calculate Open Loss
    direction_of_order = 1 if side == PositionSide.LONG else -1
    open_loss = number_of_Contract * max(0, direction_of_order * (order_price - mark_price))

    return round(initial_margin + open_loss, precision)
