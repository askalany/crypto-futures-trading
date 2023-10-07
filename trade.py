from typing import Any

from enums import PositionSide, Strategy, TickerSymbol, TIF
from repo import (
    get_available_balance,
    get_hedge_position_amount,
    get_leverage,
    get_mark_price,
    get_position_entry_price,
    new_order,
)
from strategy import trade_all_price_match_queue, trade_fixed_range


def work(order) -> Any | dict[Any, Any]:
    if "priceMatch" in order:
        return new_order(
            symbol=order["symbol"],
            side=order["side"],
            quantity=order["quantity"],
            position_side=order["positionSide"],
            price_match=order["priceMatch"],
        )
    else:
        return new_order(
            symbol=order["symbol"],
            side=order["side"],
            quantity=order["quantity"],
            position_side=order["positionSide"],
            price=order["price"],
        )


def trade(
    strategy: Strategy,
    symbol: TickerSymbol,
    position_side: PositionSide,
    buy_orders_num: int = 100,
    sell_orders_num: int = 100,
    tif: TIF = TIF.GTC,
) -> list[Any]:
    mark_price = get_mark_price(symbol=symbol)
    print(f"{mark_price=}")
    entry_price = get_position_entry_price(symbol=symbol)
    print(f"{entry_price=}")
    position_amount = get_hedge_position_amount(symbol=symbol)
    print(f"{position_amount=}")
    orders = []
    if strategy is Strategy.FIXED_RANGE:
        center_price = entry_price if entry_price > 0.0 else mark_price
        orders.extend(
            trade_fixed_range(
                symbol=symbol,
                position_side=position_side,
                center_price=center_price,
                available_balance=get_available_balance(),
                sell_amount=position_amount,
                leverage=get_leverage(symbol=symbol),
                buy_orders_num=buy_orders_num,
                sell_orders_num=sell_orders_num,
                tif=tif,
            )
        )
    elif strategy is Strategy.PRICE_MATCH_QUEUE:
        orders.extend(
            trade_all_price_match_queue(
                symbol=symbol,
                position_side=position_side,
                sell_amount=position_amount,
                tif=tif,
            )
        )
    return orders


def get_max_buy_amount(symbol: TickerSymbol):
    return (get_leverage(symbol=symbol) * get_available_balance()) / get_mark_price(
        symbol=symbol
    )
