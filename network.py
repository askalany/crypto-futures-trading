import asyncio
import logging
import time

from binance.cm_futures import CMFutures as Client
from binance.error import ClientError
from requests.adapters import HTTPAdapter
from rich.logging import RichHandler

from cm.cmmodels import AccountResponse, Balance, OrderBookResponse, PositionInformation
from rich import print


FORMAT = "%(message)s"
logging.basicConfig(level=logging.ERROR, format=FORMAT, datefmt="[%X]", handlers=[RichHandler(markup=True)])

base_url = "https://testnet.binancefuture.com"


def get_client(key, secret):
    c = Client(key=key, secret=secret, base_url=base_url)
    adapter = HTTPAdapter(pool_connections=200, pool_maxsize=200)
    c.session.mount("https://", adapter)
    global client
    client = c


def get_account() -> AccountResponse | None:
    result = None
    try:
        response = client.account(recvWindow=6000)
        result = AccountResponse(**response)
    except ClientError as error:
        logging.error(
            f"Found error. status: {error.status_code}, error code: {error.error_code}, error message: {error.error_message}"
        )
    finally:
        return result


def get_position_information(symbol) -> PositionInformation | None:
    result = None
    try:
        response = client.get_position_risk(symbol=symbol, recvWindow=6000)
        position_information_response = [
            PositionInformation(**position_information) for position_information in response
        ]
        result = list(filter(lambda x: x.symbol == symbol and x.positionSide == "LONG", position_information_response))[
            0
        ]
    except ClientError as error:
        logging.error(
            f"Found error. status: {error.status_code}, error code: {error.error_code}, error message: {error.error_message}"
        )
    finally:
        return result


def get_balance(asset) -> Balance | None:
    result = None
    try:
        response = client.balance(recvWindow=6000)
        account_balance_response = [Balance(**balance) for balance in response]
        result = list(filter(lambda x: x.asset == asset, account_balance_response))[0]
    except ClientError as error:
        logging.error(
            f"Found error. status: {error.status_code}, error code: {error.error_code}, error message: {error.error_message}"
        )
    finally:
        return result


def new_order(symbol, side, position_side, quantity: float, price: float):
    try:
        response = client.new_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            positionSide=position_side,
            quantity=quantity,
            timeInForce="GTC",
            price=price,
        )
        logging.info(response)
    except ClientError as error:
        logging.error(
            f"Found error. status: {error.status_code}, error code: {error.error_code}, error message: {error.error_message}"
        )


def new_market_order(symbol, side, position_side, quantity: float):
    try:
        response = client.new_order(
            symbol=symbol, side=side, type="MARKET", positionSide=position_side, quantity=quantity, recvWindow=6000
        )
        logging.info(response)
    except ClientError as error:
        logging.error(
            f"Found error. status: {error.status_code}, error code: {error.error_code}, error message: {error.error_message}"
        )


def cancel_all_orders(symbol):
    try:
        response = client.cancel_open_orders(symbol=symbol)
        logging.info(response)
    except ClientError as error:
        logging.error(
            f"Found error. status: {error.status_code}, error code: {error.error_code}, error message: {error.error_message}"
        )


async def get_depth(symbol: str, limit: int = 50) -> OrderBookResponse | None:
    result = None
    try:
        response = client.depth(symbol=symbol, limit=limit)
        logging.info(response)
        result = OrderBookResponse(**response)
    except ClientError as error:
        logging.error(
            f"Found error. status: {error.status_code}, error code: {error.error_code}, error message: {error.error_message}"
        )
    finally:
        return result


async def main():
    get_client(
        key="d45caa464dd967a905316d222bd417b25fb573b1ea0c8af15674c3378f1a1eb0",
        secret="a7494661ffc12bacfc6208f8d907e506764e1a8da72ac38bd92b5e4d5e934781",
    )
    print(f"started main at {time.strftime('%X')}")
    async with asyncio.TaskGroup() as tg:
        task1: asyncio.Task = tg.create_task(get_depth("BTCUSD_PERP", limit=5))
        task2: asyncio.Task = tg.create_task(get_depth("BTCUSD_PERP", limit=50))
    print(f"Task 1: {task1.result()}")
    print(f"Task 2: {task2.result()}")
    print(f"finished main at {time.strftime('%X')}")


if __name__ == "__main__":
    asyncio.run(main())
