import logging
from typing import Any

from binance.error import ClientError
from binance.um_futures import UMFutures
from requests.adapters import HTTPAdapter

from consts import BASE_URL, KEY, SECRET

adapter = HTTPAdapter(pool_connections=200, pool_maxsize=200)

client = UMFutures(key=KEY, secret=SECRET, base_url=BASE_URL)
client.session.mount("https://", adapter)


def log_client_error(error: ClientError) -> None:
    logging.error(f"{error.status_code=}, {error.error_code=}, {error.error_message=}")


def cancel_all_orders_request(
    symbol, receive_window: int = 6000
) -> Any | dict[Any, Any]:
    response = {}
    try:
        response = client.cancel_open_orders(symbol=symbol, recvWindow=receive_window)
    except ClientError as error:
        log_client_error(error)
    finally:
        return response


def new_price_match_order_request(
    symbol: str,
    side: str,
    quantity: float,
    position_side: str,
    order_type: str,
    time_in_force: str,
    price_match: str,
) -> Any | dict[Any, Any]:
    response = {}
    try:
        response = client.new_order(
            symbol=symbol,
            side=side,
            positionSide=position_side,
            type=order_type,
            quantity=quantity,
            timeInForce=time_in_force,
            priceMatch=price_match,
        )
    except ClientError as error:
        log_client_error(error)
    finally:
        return response


def new_order_request(
    symbol: str,
    side: str,
    quantity: float,
    position_side: str,
    price: float,
    order_type: str,
    time_in_force: str,
) -> Any | dict[Any, Any]:
    response = {}
    try:
        response = client.new_order(
            symbol=symbol,
            side=side,
            positionSide=position_side,
            type=order_type,
            quantity=str(quantity),
            timeInForce=time_in_force,
            price=price,
        )
    except ClientError as error:
        log_client_error(error)
    finally:
        return response


def new_batch_order_request(params) -> Any | dict[Any, Any]:
    response = {}
    try:
        response = client.new_batch_order(batchOrders=params)
    except ClientError as error:
        log_client_error(error)
    finally:
        return response


def get_position_risk_request(symbol: str) -> Any | dict[Any, Any]:
    response = {}
    try:
        response = client.get_position_risk(symbol=symbol, recvWindow=6000)
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
        # noinspection PyCallingNonCallable
        response = client.account(recvWindow=6000)
    except ClientError as error:
        log_client_error(error)
    finally:
        return response


def get_mark_price_request(symbol: str) -> Any | dict[Any, Any]:
    response = {}
    try:
        response = client.mark_price(symbol=symbol)
    except ClientError as error:
        log_client_error(error)
    finally:
        return response


def get_listen_key_request() -> Any | dict[Any, Any]:
    response = {}
    try:
        response = client.new_listen_key()
    except ClientError as error:
        log_client_error(error)
    finally:
        return response


def close_listen_key_request(listen_key: str) -> Any | dict[Any, Any]:
    response = {}
    try:
        response = client.close_listen_key(listenKey=listen_key)
    except ClientError as error:
        log_client_error(error)
    finally:
        return response


def get_open_orders_request(symbol: str) -> Any | dict[Any, Any]:
    response = {}
    try:
        response = client.get_open_orders(symbol=symbol)
    except ClientError as error:
        log_client_error(error)
    finally:
        return response


def keep_alive_request(listen_key: str):
    response = {}
    try:
        response = client.renew_listen_key(listenKey=listen_key)
    except ClientError as error:
        log_client_error(error)
    finally:
        return response


def get_time_request() -> Any | dict[Any, Any]:
    response = {}
    try:
        response = client.time()
    except ClientError as error:
        log_client_error(error)
    finally:
        return response
