from ast import List
import logging
from typing import Any

from binance.error import ClientError
from binance.um_futures import UMFutures
from requests.adapters import HTTPAdapter

from consts import BASE_URL, KEY, SECRET

adapter = HTTPAdapter(pool_connections=200, pool_maxsize=200)

um_futures_client = UMFutures(key=KEY, secret=SECRET, base_url=BASE_URL)
um_futures_client.session.mount("https://", adapter)


def log_client_error(error: ClientError) -> None:
    logging.error(f"{error.status_code=}, {error.error_code=}, {error.error_message=}")


def cancel_all_orders_request(symbol, recvWindow: int = 2000) -> Any | dict[Any, Any]:
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
    response = {}
    try:
        response = um_futures_client.new_batch_order(batchOrders=params)
    except ClientError as error:
        log_client_error(error)
    finally:
        return response


def get_position_risk_request(symbol: str) -> Any | dict[Any, Any]:
    response = {}
    try:
        response = um_futures_client.get_position_risk(symbol=symbol, recvWindow=6000)
    except ClientError as error:
        log_client_error(error)
    finally:
        return response


def get_leverage_request(symbol: str) -> Any | dict[Any, Any]:
    response = {}
    try:
        response = get_position_risk_request(symbol=symbol)
    except ClientError as error:
        log_client_error(error)
    finally:
        return response


def get_account_info_request() -> Any | dict[Any, Any]:
    response = {}
    try:
        response = um_futures_client.account(recvWindow=6000)
    except ClientError as error:
        log_client_error(error)
    finally:
        return response


def get_mark_price_request(symbol: str) -> Any | dict[Any, Any]:
    response = {}
    try:
        response = um_futures_client.mark_price(symbol=symbol)
    except ClientError as error:
        log_client_error(error)
    finally:
        return response


def get_listen_key_request() -> Any | dict[Any, Any]:
    response = {}
    try:
        response = um_futures_client.new_listen_key()
    except ClientError as error:
        log_client_error(error)
    finally:
        return response


def close_listen_key_request(listenKey: str) -> Any | dict[Any, Any]:
    response = {}
    try:
        response = um_futures_client.close_listen_key(listenKey=listenKey)
    except ClientError as error:
        log_client_error(error)
    finally:
        return response


def get_open_orders_request(symbol: str) -> Any | dict[Any, Any]:
    response = {}
    try:
        response = um_futures_client.get_open_orders(symbol=symbol)
    except ClientError as error:
        log_client_error(error)
    finally:
        return response


def keep_alive_request(listenKey: str):
    response = {}
    try:
        response = um_futures_client.renew_listen_key(listenKey=listenKey)
    except ClientError as error:
        log_client_error(error)
    finally:
        return response
