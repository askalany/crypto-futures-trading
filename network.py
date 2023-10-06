from ast import List
import logging
from typing import Any

from binance.error import ClientError
from binance.um_futures import UMFutures
from requests.adapters import HTTPAdapter

from consts import BASE_URL, KEY, SECRET

adapter = HTTPAdapter(pool_connections=200, pool_maxsize=200)

um_futures_client = UMFutures(key=KEY, secret=SECRET, base_url=BASE_URL)


def log_client_error(error: ClientError) -> None:
    """
    The function logs the details of a client error.

    :param error: The parameter `error` is of type `ClientError`
    :type error: ClientError
    """
    logging.error(f"{error.status_code=}, {error.error_code=}, {error.error_message=}")


def cancel_all_orders_request(symbol, recvWindow: int = 2000) -> Any | dict[Any, Any]:
    """
    The function cancels all open orders for a given symbol in a futures trading platform.

    :param symbol: The symbol parameter represents the trading pair symbol for which you want to cancel
    all open orders. For example, if you want to cancel all open orders for the BTC/USDT trading pair,
    you would pass "BTCUSDT" as the symbol parameter
    :param recvWindow: The `recvWindow` parameter is an optional parameter that specifies the number of
    milliseconds the request is valid for. It is used to ensure that the request is processed within a
    certain time frame. If the request takes longer than the specified `recvWindow` value, it will be
    rejected. The default value, defaults to 2000
    :type recvWindow: int (optional)
    :return: a response object.
    """
    response = {}
    try:
        response = um_futures_client.cancel_open_orders(
            symbol=symbol, recvWindow=recvWindow
        )
    except ClientError as error:
        log_client_error(error)
    finally:
        return response


def new_price_match_order_request(
    symbol: str,
    side: str,
    quantity: float,
    positionSide: str,
    type: str,
    timeInForce: str,
    priceMatch: str,
) -> Any | dict[Any, Any]:
    """
    The function `new_price_match_order_request` sends a new order request to a futures client with the
    specified parameters and returns the response.

    :param symbol: The symbol parameter represents the trading pair symbol, such as "BTCUSDT" for
    Bitcoin against USDT (Tether)
    :type symbol: str
    :param side: The "side" parameter in the function represents the side of the order, which can be
    either "BUY" or "SELL"
    :type side: str
    :param quantity: The quantity parameter represents the amount of the asset that you want to buy or
    sell in the order. It is a float value, which means it can have decimal places
    :type quantity: float
    :param positionSide: The parameter "positionSide" is used to specify the position side of the order.
    It can have two possible values: "LONG" or "SHORT"
    :type positionSide: str
    :param type: The "type" parameter specifies the type of order to be placed. It can have values like
    "LIMIT", "MARKET", "STOP_MARKET", etc
    :type type: str
    :param timeInForce: The "timeInForce" parameter is used to specify how long the order will remain
    active before it is either executed or canceled. It can have the following values:
    :type timeInForce: str
    :param priceMatch: The "priceMatch" parameter in the function is used to specify the price at which
    the order should be matched. It is a string parameter that can take the following values:
    :type priceMatch: str
    :return: a response object.
    """
    response = {}
    try:
        response = um_futures_client.new_order(
            symbol=symbol,
            side=side,
            positionSide=positionSide,
            type=type,
            quantity=quantity,
            timeInForce=timeInForce,
            priceMatch=priceMatch,
        )
    except ClientError as error:
        log_client_error(error)
    finally:
        return response


def new_order_request(
    symbol: str,
    side: str,
    quantity: float,
    positionSide: str,
    price: float,
    type: str,
    timeInForce: str,
) -> Any | dict[Any, Any]:
    """
    The function `new_order_request` sends a new order request to a futures trading client and returns
    the response.

    :param symbol: The symbol parameter represents the trading pair symbol for the order, such as
    "BTCUSDT" or "ETHBTC"
    :type symbol: str
    :param side: The "side" parameter represents the side of the order, whether it is a buy or sell
    order. It can have two possible values: "BUY" or "SELL"
    :type side: str
    :param quantity: The quantity parameter represents the quantity of the asset you want to buy or sell
    in the order. It is a float value
    :type quantity: float
    :param positionSide: The parameter "positionSide" is used to specify the position side of the order.
    It can have two possible values: "LONG" or "SHORT". "LONG" indicates that the order is for a long
    position, while "SHORT" indicates that the order is for a short position
    :type positionSide: str
    :param price: The "price" parameter in the "new_order_request" function is used to specify the price
    at which you want to place the order. It is of type float, which means it can accept decimal values
    :type price: float
    :param type: The "type" parameter in the "new_order_request" function is used to specify the type of
    order to be placed. It can have different values depending on the trading platform or exchange being
    used. Some common values for the "type" parameter are:
    :type type: str
    :param timeInForce: The "timeInForce" parameter in the "new_order_request" function is used to
    specify the duration for which the order will remain active before it is either executed or
    canceled. It determines how long the order will be valid in the market
    :type timeInForce: str
    :return: a response object.
    """
    response = {}
    try:
        response = um_futures_client.new_order(
            symbol=symbol,
            side=side,
            positionSide=positionSide,
            type=type,
            quantity=str(quantity),
            timeInForce=timeInForce,
            price=price,
        )
    except ClientError as error:
        log_client_error(error)
    finally:
        return response


def new_batch_order_request(params) -> Any | dict[Any, Any]:
    """
    The function `new_batch_order_request` sends a request to a futures client to place a new batch
    order and returns the response.

    :param params: The `params` parameter is a dictionary that contains the necessary information for
    creating a new batch order request. The specific keys and values in the dictionary will depend on
    the requirements of the `um_futures_client.new_batch_order()` function
    :return: the response from the `um_futures_client.new_batch_order(params)` method.
    """
    response = {}
    try:
        response = um_futures_client.new_batch_order(batchOrders=params)
    except ClientError as error:
        log_client_error(error)
    finally:
        return response


def get_position_risk_request(symbol: str) -> Any | dict[Any, Any]:
    """
    The function `get_position_risk_request` retrieves the position risk for a given symbol using the
    `um_futures_client` API, and returns the response.

    :param symbol: The symbol parameter is a string that represents the trading pair or instrument
    symbol for which you want to retrieve the position risk information. For example, it could be
    "BTCUSDT" for the Bitcoin to USDT trading pair
    :type symbol: str
    :return: a response object.
    """
    response = {}
    try:
        response = um_futures_client.get_position_risk(symbol=symbol, recvWindow=6000)
    except ClientError as error:
        log_client_error(error)
    finally:
        return response


def get_leverage_request(symbol: str) -> Any | dict[Any, Any]:
    """
    The function `get_leverage_request` attempts to retrieve position risk information for a given
    symbol and returns the response, or logs any client errors encountered.

    :param symbol: The symbol parameter is a string that represents the trading symbol of a financial
    instrument, such as a stock or a cryptocurrency
    :type symbol: str
    :return: a dictionary object.
    """
    response = {}
    try:
        response = get_position_risk_request(symbol=symbol)
    except ClientError as error:
        log_client_error(error)
    finally:
        return response


def get_account_info_request() -> Any | dict[Any, Any]:
    """
    The function `get_account_info_request` retrieves account information from a futures client,
    handling any potential errors.
    :return: the response from the `um_futures_client.account()` method.
    """
    response = {}
    try:
        response = um_futures_client.account(recvWindow=6000)
    except ClientError as error:
        log_client_error(error)
    finally:
        return response


def get_mark_price_request(symbol: str) -> Any | dict[Any, Any]:
    """
    The function `get_mark_price_request` sends a request to the UM Futures API to get the mark price
    for a given symbol and returns the response.

    :param symbol: The `symbol` parameter is a string that represents the trading pair symbol for which
    you want to get the mark price
    :type symbol: str
    :return: a response, which is a dictionary.
    """
    response = {}
    try:
        response = um_futures_client.mark_price(symbol=symbol)
    except ClientError as error:
        log_client_error(error)
    finally:
        return response


def get_listen_key_request() -> Any | dict[Any, Any]:
    """
    The function `get_listen_key_request` sends a request to create a new listen key and returns the
    response.
    :return: The `get_listen_key_request` function is returning a response object.
    """
    response = {}
    try:
        response = um_futures_client.new_listen_key()
    except ClientError as error:
        log_client_error(error)
    finally:
        return response


def close_listen_key_request(listenKey: str) -> Any | dict[Any, Any]:
    """
    The function `close_listen_key_request` closes a listen key using the `um_futures_client` and
    returns the response.

    :param listenKey: The listenKey parameter is a string that represents a unique identifier for a
    user's WebSocket connection. It is typically used in API calls to close the WebSocket connection and
    stop receiving updates
    :type listenKey: str
    :return: a response, which is a dictionary.
    """
    response = {}
    try:
        response = um_futures_client.close_listen_key(listenKey=listenKey)
    except ClientError as error:
        log_client_error(error)
    finally:
        return response


def get_open_orders_request(symbol: str) -> Any | dict[Any, Any]:
    """
    The function `get_open_orders_request` retrieves open orders for a given symbol using the
    `um_futures_client` and handles any potential errors.

    :param symbol: The symbol parameter is a string that represents the trading pair or symbol for which
    you want to retrieve the open orders. It could be something like "BTCUSDT" for the Bitcoin to USDT
    trading pair
    :type symbol: str
    :return: the response from the `um_futures_client.get_open_orders` method.
    """
    response = {}
    try:
        response = um_futures_client.get_open_orders(symbol=symbol)
    except ClientError as error:
        log_client_error(error)
    finally:
        return response
