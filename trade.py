from typing import Any

from enums import TIF, PositionSide, Strategy, TickerSymbol
from repo import get_available_balance, get_leverage, new_batch_order, new_order
from strategy import trade_all_price_match_queue, trade_fixed_range


def work(order) -> Any | dict[Any, Any]:
    if isinstance(order, list):
        return new_batch_order(orders=order)
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
    mark_price: float,
    entry_price: float,
    position_amount: float,
    buy_orders_num: int = 100,
    sell_orders_num: int = 100,
    tif: TIF = TIF.GTC,
) -> list[Any]:
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
