from enums import (
    TIF,
    OrderType,
    PositionSide,
    PriceMatch,
    PriceMatchNone,
    Side,
    TickerSymbol,
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
    new_order_request,
    new_price_match_order_request,
)


def get_hedge_position_amount(symbol: TickerSymbol):
    return float(get_position_risk_request(symbol=symbol.name)[0]["positionAmt"])


def get_available_balance():
    return float(get_account_info_request()["availableBalance"])


def get_mark_price(symbol: TickerSymbol):
    return float(get_mark_price_request(symbol.name)["markPrice"])


def new_order(
    symbol: TickerSymbol,
    side: Side,
    quantity: float,
    positionSide: PositionSide,
    price: float = -1.0,
    type: OrderType = OrderType.LIMIT,
    timeInForce: TIF = TIF.GTC,
    priceMatch: PriceMatch = PriceMatchNone.NONE,
):
    if priceMatch is PriceMatchNone.NONE:
        return new_order_request(
            symbol=symbol.name,
            side=side.name,
            quantity=quantity,
            positionSide=positionSide.name,
            price=price,
            type=type.name,
            timeInForce=timeInForce.name,
        )
    else:
        return new_price_match_order_request(
            symbol=symbol.name,
            side=side.name,
            quantity=quantity,
            positionSide=positionSide.name,
            type=type.name,
            timeInForce=timeInForce.name,
            priceMatch=priceMatch.name,
        )


def get_leverage(symbol: TickerSymbol):
    position_risk = get_leverage_request(symbol.name)
    return int(position_risk[0]["leverage"])


def cancel_all_orders(symbol: TickerSymbol):
    return cancel_all_orders_request(symbol.name)


def get_listen_key():
    return get_listen_key_request()["listenKey"]


def close_listen_key(listenKey):
    return close_listen_key_request(listenKey)


def get_open_orders(symbol: TickerSymbol):
    return get_open_orders_request(symbol.name)
