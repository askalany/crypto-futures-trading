from enum import Enum
import json
from typing import Any
from rich import print
from enums import (
    OrderType,
    PositionSide,
    PriceMatch,
    PriceMatchNone,
    Side,
    TickerSymbol,
    TIF,
)
from network import (
    cancel_all_orders_request,
    close_listen_key_request,
    get_account_info_request,
    get_leverage_request,
    get_listen_key_request,
    get_mark_price_request,
    get_open_orders_request,
    get_position_risk_request,
    keep_alive_request,
    new_batch_order_request,
    new_order_request,
    new_price_match_order_request,
    get_time_request,
)


def get_position_risk(
    symbol: TickerSymbol,
) -> tuple[
    float,
    float,
    str,
    str,
    float,
    int,
    float,
    float,
    float,
    float,
    float,
    float,
    str,
    float,
    str,
    float,
]:
    position_risk = get_position_risk_request(symbol=symbol.name)[0]
    return (
        float(position_risk["entryPrice"]),
        float(position_risk["breakEvenPrice"]),
        str(position_risk["marginType"]),
        str(position_risk["isAutoAddMargin"]),
        float(position_risk["isolatedMargin"]),
        int(position_risk["leverage"]),
        float(position_risk["liquidationPrice"]),
        float(position_risk["markPrice"]),
        float(position_risk["maxNotionalValue"]),
        float(position_risk["positionAmt"]),
        float(position_risk["notional"]),
        float(position_risk["isolatedWallet"]),
        str(position_risk["symbol"]),
        float(position_risk["unRealizedProfit"]),
        str(position_risk["positionSide"]),
        float(position_risk["updateTime"]),
    )


def get_hedge_position_amount(symbol: TickerSymbol) -> float:
    return float(get_position_risk_request(symbol=symbol.name)[0]["positionAmt"])


def get_position_entry_price(symbol: TickerSymbol) -> float:
    return float(get_position_risk_request(symbol=symbol.name)[0]["entryPrice"])


def get_position_unrealized_profit(symbol: TickerSymbol) -> float:
    return float(get_position_risk_request(symbol=symbol.name)[0]["unRealizedProfit"])


def get_available_balance() -> float:
    return float(get_account_info_request()["availableBalance"])


def get_mark_price(symbol: TickerSymbol) -> float:
    return float(get_mark_price_request(symbol=symbol.name)["markPrice"])


def new_order(
    symbol: TickerSymbol,
    side: Side,
    quantity: float,
    position_side: PositionSide,
    price: float = -1.0,
    order_type: OrderType = OrderType.LIMIT,
    time_in_force: TIF = TIF.GTC,
    price_match: PriceMatch = PriceMatchNone.NONE,
) -> Any | dict[Any, Any]:
    return (
        new_order_request(
            symbol=symbol.name,
            side=side.name,
            quantity=quantity,
            position_side=position_side.name,
            price=price,
            order_type=order_type.name,
            time_in_force=time_in_force.name,
        )
        if price_match is PriceMatchNone.NONE
        else new_price_match_order_request(
            symbol=symbol.name,
            side=side.name,
            quantity=quantity,
            position_side=position_side.name,
            order_type=order_type.name,
            time_in_force=time_in_force.name,
            price_match=price_match.name,
        )
    )


def new_batch_order(orders: list) -> Any | dict[Any, Any]:
    new_orders = []
    for order in orders:
        new_dict = {}
        for key in order:
            key_value = order[key]
            if isinstance(key_value, Enum):
                new_dict[key] = key_value.value
            else:
                new_dict[key] = str(key_value)
        new_orders.append(new_dict)
    return new_batch_order_request(params=new_orders)


def get_leverage(symbol: TickerSymbol) -> int:
    return int(get_leverage_request(symbol=symbol.name)[0]["leverage"])


def cancel_all_orders(symbol: TickerSymbol) -> Any | dict[Any, Any]:
    return cancel_all_orders_request(symbol=symbol.name)


def get_listen_key() -> str:
    return get_listen_key_request()["listenKey"]


def close_listen_key(listen_key: str) -> Any | dict[Any, Any]:
    return close_listen_key_request(listen_key=listen_key)


def get_open_orders(symbol: TickerSymbol) -> Any | dict[Any, Any]:
    return get_open_orders_request(symbol=symbol.name)


def keep_alive(listen_key: str):
    return keep_alive_request(listen_key=listen_key)


def get_time() -> int:
    return get_time_request()["serverTime"]
