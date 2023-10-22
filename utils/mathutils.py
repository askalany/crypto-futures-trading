import numpy as np

from data.enums import PositionSide


def get_geom_scale(orders_num: int, high_price: float, low_price: float) -> list[float]:
    return np.geomspace(
        start=low_price, stop=high_price, num=orders_num, dtype=np.float64
    ).tolist()


def get_linear_scale(
    orders_num: int, high_price: float, low_price: float
) -> list[float]:
    return np.linspace(
        start=low_price, stop=high_price, num=orders_num, dtype=np.float64
    ).tolist()


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


def make_it_smaller(total_amount: float, final_scaled: list[float]) -> list[float]:
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
    open_loss = number_of_Contract * abs(
        min(0, direction_of_order * (mark_price - order_price))
    )
    return round(initial_margin + open_loss, precision)
