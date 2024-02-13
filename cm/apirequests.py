import logging

from binance.cm_futures import CMFutures as Client
from binance.error import ClientError
from requests.adapters import HTTPAdapter
from rich.logging import RichHandler

from cmmodels import AccountResponse, Balance, PositionInformation


FORMAT = "%(message)s"
logging.basicConfig(level=logging.ERROR, format=FORMAT, datefmt="[%X]", handlers=[RichHandler(markup=True)])

base_url = "https://testnet.binancefuture.com"

def get_client(key, secret):
    c = Client(key=key, secret=secret, base_url=base_url)
    adapter = HTTPAdapter(pool_connections=200, pool_maxsize=200)
    c.session.mount("https://", adapter)
    global client
    client = c




def get_account() -> AccountResponse:
    try:
        response = client.account(recvWindow=6000)
        return AccountResponse(**response)
    except ClientError as error:
        logging.error(
            f"Found error. status: {error.status_code}, error code: {error.error_code}, error message: {error.error_message}"
        )


def get_position_information(symbol) -> PositionInformation:
    try:
        response = client.get_position_risk(symbol=symbol, recvWindow=6000)
        position_information_response = [
            PositionInformation(**position_information) for position_information in response
        ]
        return list(filter(lambda x: x.symbol == symbol and x.positionSide == "LONG", position_information_response))[0]
    except ClientError as error:
        logging.error(
            f"Found error. status: {error.status_code}, error code: {error.error_code}, error message: {error.error_message}"
        )


def get_balance(asset) -> Balance:
    try:
        response = client.balance(recvWindow=6000)
        account_balance_response = [Balance(**balance) for balance in response]
        return list(filter(lambda x: x.asset == asset, account_balance_response))[0]
    except ClientError as error:
        logging.error(
            f"Found error. status: {error.status_code}, error code: {error.error_code}, error message: {error.error_message}"
        )


def new_order(symbol, side, position_side, quantity: float, price: float):
    try:
        response = client.new_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            positionSide=position_side,
            quantity=quantity,
            timeInForce="GTC",
            price=price        )
        logging.info(response)
    except ClientError as error:
        logging.error(
            f"Found error. status: {error.status_code}, error code: {error.error_code}, error message: {error.error_message}"
        )

def new_market_order(symbol, side, position_side, quantity: float):
    try:
        response = client.new_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            positionSide=position_side,
            quantity=quantity,
            recvWindow=6000,
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
