from typing import Any
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


def get_hedge_position_amount(symbol: TickerSymbol) -> float:
    """
    The function `get_hedge_position_amount` returns the position amount of a given symbol.

    :param symbol: The parameter `symbol` is of type `TickerSymbol`
    :type symbol: TickerSymbol
    :return: the position amount as a float.
    """
    return float(get_position_risk_request(symbol=symbol.name)[0]["positionAmt"])


def get_available_balance() -> float:
    """
    The function `get_available_balance` returns the available balance from an account information
    request.
    :return: The available balance of the account as a float value.
    """
    return float(get_account_info_request()["availableBalance"])


def get_mark_price(symbol: TickerSymbol) -> float:
    """
    The function `get_mark_price` takes a `TickerSymbol` object as input and returns the mark price of
    the symbol.

    :param symbol: The parameter `symbol` is of type `TickerSymbol`
    :type symbol: TickerSymbol
    :return: the mark price of a given ticker symbol as a float value.
    """
    return float(get_mark_price_request(symbol=symbol.name)["markPrice"])


def new_order(
    symbol: TickerSymbol,
    side: Side,
    quantity: float,
    positionSide: PositionSide,
    price: float = -1.0,
    type: OrderType = OrderType.LIMIT,
    timeInForce: TIF = TIF.GTC,
    priceMatch: PriceMatch = PriceMatchNone.NONE,
) -> Any | dict[Any, Any]:
    """
    The `new_order` function takes in various parameters to create a new order request and returns the
    appropriate request based on the provided parameters.

    :param symbol: The symbol parameter represents the ticker symbol of the asset being traded. It
    should be of type TickerSymbol
    :type symbol: TickerSymbol
    :param side: The "side" parameter in the "new_order" function represents the side of the order,
    which can be either "BUY" or "SELL"
    :type side: Side
    :param quantity: The quantity parameter represents the quantity of the asset you want to buy or sell
    in the order. It is a float value
    :type quantity: float
    :param positionSide: The parameter "positionSide" is used to specify the position side of the order.
    It can have two possible values: "LONG" or "SHORT". This parameter is used to indicate whether the
    order is for a long position (buying) or a short position (selling)
    :type positionSide: PositionSide
    :param price: The `price` parameter in the `new_order` function is used to specify the price at
    which the order should be executed. It is an optional parameter with a default value of -1.0. If a
    specific price is not provided, the order will be placed at the market price
    :type price: float
    :param type: The `type` parameter in the `new_order` function is used to specify the type of order
    to be placed. It is an optional parameter with a default value of `OrderType.LIMIT`
    :type type: OrderType
    :param timeInForce: The `timeInForce` parameter is used to specify how long the order will remain
    active before it is automatically canceled. It can take one of the following values:
    :type timeInForce: TIF
    :param priceMatch: The `priceMatch` parameter is an optional parameter that specifies the type of
    price matching to be used for the order. It is of type `PriceMatch` which is an enumeration with
    possible values:
    :type priceMatch: PriceMatch
    :return: The function `new_order` returns either a `new_order_request` or a
    `new_price_match_order_request` depending on the value of `priceMatch`.
    """
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


def get_leverage(symbol: TickerSymbol) -> int:
    """
    The function `get_leverage` takes a `TickerSymbol` object as input, sends a request to get the
    leverage for that symbol, and returns the leverage as an integer.

    :param symbol: The parameter "symbol" is of type "TickerSymbol"
    :type symbol: TickerSymbol
    :return: an integer value representing the leverage for a given ticker symbol.
    """
    position_risk = get_leverage_request(symbol=symbol.name)
    return int(position_risk[0]["leverage"])


def cancel_all_orders(symbol: TickerSymbol) -> Any | dict[Any, Any]:
    """
    The function cancels all orders for a given ticker symbol.

    :param symbol: The parameter "symbol" is of type "TickerSymbol"
    :type symbol: TickerSymbol
    :return: The cancel_all_orders_request function is being returned.
    """
    return cancel_all_orders_request(symbol=symbol.name)


def get_listen_key() -> str:
    """
    The function `get_listen_key` returns the listen key obtained from a request to the
    `get_listen_key_request` function.
    :return: the value of the "listenKey" key from the response of the "get_listen_key_request()"
    function.
    """
    return get_listen_key_request()["listenKey"]


def close_listen_key(listenKey) -> Any | dict[Any, Any]:
    """
    The function "close_listen_key" takes a listenKey as input and returns the result of a
    close_listen_key_request.

    :param listenKey: The listenKey parameter is a unique identifier that is used to establish a
    WebSocket connection for receiving real-time updates from a server
    :return: the result of the `close_listen_key_request` function, which is not specified in the given
    code.
    """
    return close_listen_key_request(listenKey=listenKey)


def get_open_orders(symbol: TickerSymbol) -> Any | dict[Any, Any]:
    """
    The function `get_open_orders` takes a `TickerSymbol` object as input and returns the result of a
    request for open orders for that symbol.

    :param symbol: The parameter `symbol` is of type `TickerSymbol`
    :type symbol: TickerSymbol
    :return: the result of the `get_open_orders_request` function call.
    """
    return get_open_orders_request(symbol=symbol.name)
