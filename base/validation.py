from typing import Any

from base.error import ParameterRequiredError, ParameterTypeError, ParameterValueError
from data.enums import TIF, PositionSide, Strategy, TickerSymbol


def check_required_parameter(value, name):
    if not value and value != 0:
        raise ParameterRequiredError([name])


def check_required_parameters(params):
    for p in params:
        check_required_parameter(p[0], p[1])


def check_enum_parameter(value, enum_class):
    if value not in {item.value for item in enum_class}:
        raise ParameterValueError([value])


def check_type_parameter(value, name, data_type):
    if value is not None and not isinstance(value, data_type):
        raise ParameterTypeError([name, data_type])


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
    price_sell_max_mult: float,
    price_sell_min_mult: float,
    price_buy_max_mult: float,
    price_buy_min_mult: float,
) -> tuple[bool, bool, float, TickerSymbol, Strategy, PositionSide, int, int, TIF, float, float, float, float]:
    if not isinstance(once, bool):
        raise ValueError("incorrect input for once")
    if not isinstance(use_mark_price, bool):
        raise ValueError("incorrect input for use_mark_price")
    if not isinstance(delay_seconds, float):
        raise ValueError("incorrect input for delay_seconds")
    if not isinstance(symbol, TickerSymbol):
        raise ValueError("incorrect input for symbol")
    if not isinstance(strategy, Strategy):
        raise ValueError("incorrect input for strategy")
    if not isinstance(position_side, PositionSide):
        raise ValueError("incorrect input for position_side")
    if not isinstance(tif, TIF):
        raise ValueError("incorrect input for tif")
    if not isinstance(price_sell_max_mult, float):
        raise ValueError("incorrect input for price_sell_max_mult")
    if not isinstance(price_sell_min_mult, float):
        raise ValueError("incorrect input for price_sell_min_mult")
    if not isinstance(price_buy_max_mult, float):
        raise ValueError("incorrect input for price_buy_max_mult")
    if not isinstance(price_buy_min_mult, float):
        raise ValueError("incorrect input for price_buy_min_mult")
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
        price_sell_max_mult,
        price_sell_min_mult,
        price_buy_max_mult,
        price_buy_min_mult
    )
