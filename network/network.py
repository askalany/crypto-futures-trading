import logging
from typing import Any

from base.Singleton import Singleton
from binance.um_futures import UMFutures
from data.enums import TimeInForce
from model import AccountInformation, OrderBook
from model import CancelAllOpenOrders
from model import ChangeInitialLeverage
from network.responses.responses import ListenKeyResponse
from network.responses.responses import MarkPriceResponse
from network.responses.responses import PositionInformationResponse
from binance.error import ClientError


def client_error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ClientError as error:
            handle_client_error(error)

    return wrapper


def handle_client_error(error: ClientError):
    logging.error(
        f"Found error. status: {error.status_code}, error code: {error.error_code}, error message: {error.error_message}"
    )


class BinanceNetworkClient(metaclass=Singleton):
    def __init__(self, client: UMFutures):
        self.client = client

    @client_error_handler
    def cancel_all_orders_request(self, symbol) -> CancelAllOpenOrders:
        response = self.client.cancel_open_orders(symbol=symbol)
        logging.info(response)
        return CancelAllOpenOrders(**response)

    @client_error_handler
    def new_price_match_order_request(
        self,
        symbol: str,
        side: str,
        quantity: float,
        position_side: str,
        order_type: str,
        time_in_force: str,
        price_match: str,
    ) -> Any | dict[Any, Any]:
        response = self.client.new_order(
            symbol=symbol,
            side=side,
            positionSide=position_side,
            type=order_type,
            quantity=quantity,
            timeInForce=time_in_force,
            priceMatch=price_match,
        )
        logging.info(response)
        return response

    @client_error_handler
    def new_order_request(
        self,
        symbol: str,
        side: str,
        quantity: float,
        position_side: str,
        order_type: str,
        price: float = 0.0,
        time_in_force: str = TimeInForce.GTC.name,
    ) -> Any | dict[Any, Any]:
        response = (
            self.client.new_order(
                symbol=symbol,
                side=side,
                positionSide=position_side,
                type=order_type,
                quantity=str(quantity),
                timeInForce=time_in_force,
                price=price,
            )
            if time_in_force is not None and price is not None
            else self.client.new_order(
                symbol=symbol,
                side=side,
                positionSide=position_side,
                type=order_type,
                quantity=str(quantity),
                recvWindow=6000,
            )
        )
        logging.info(response)
        return response

    @client_error_handler
    def new_reduce_only_order_request(
        self,
        symbol: str,
        side: str,
        quantity: float,
        position_side: str,
        order_type: str,
        price: float = 0.0,
        time_in_force: str = TimeInForce.GTC.name,
    ) -> Any | dict[Any, Any]:
        response = (
            self.client.new_order(
                symbol=symbol,
                side=side,
                positionSide=position_side,
                type=order_type,
                quantity=str(quantity),
                reduceOnly="true",
                timeInForce=time_in_force,
                price=price,
            )
            if time_in_force is not None and price is not None
            else self.client.new_order(
                symbol=symbol,
                side=side,
                positionSide=position_side,
                type=order_type,
                quantity=str(quantity),
                reduceOnly="true",
                recvWindow=6000,
            )
        )
        logging.info(response)
        return response

    @client_error_handler
    def new_batch_order_request(self, params) -> Any | dict[Any, Any]:
        logging.info(f"batch_order_request={params}")
        response = self.client.new_batch_order(batchOrders=params)
        logging.info(response)
        return response

    @client_error_handler
    def get_position_risk_request(self, symbol: str) -> list[PositionInformationResponse]:
        response = self.client.get_position_risk(symbol=symbol)
        # logging.info(response)
        return [PositionInformationResponse(**i) for i in response]

    @client_error_handler
    def get_account_info_request(self) -> AccountInformation:
        response = self.client.account()
        # logging.info(response)
        return AccountInformation(**response)

    @client_error_handler
    def get_mark_price_request(self, symbol: str) -> MarkPriceResponse:
        response = self.client.mark_price(symbol=symbol)
        # logging.info(response)
        return MarkPriceResponse(**response)

    @client_error_handler
    def get_ticker_price_request(self, symbol: str) -> Any | dict[Any, Any]:
        response = self.client.ticker_price(symbol=symbol)
        # logging.info(response)
        return response

    @client_error_handler
    def get_listen_key_request(self) -> ListenKeyResponse:
        response = self.client.new_listen_key()
        # logging.info(response)
        return ListenKeyResponse(**response)

    @client_error_handler
    def close_listen_key_request(self, listen_key: str) -> Any | dict[Any, Any]:
        response = self.client.close_listen_key(listenKey=listen_key)
        # logging.info(response)
        return response

    @client_error_handler
    def get_open_orders_request(self, symbol: str) -> Any | dict[Any, Any]:
        response = self.client.get_open_orders(symbol=symbol)
        # logging.info(response)
        return response

    @client_error_handler
    def keep_alive_request(self, listen_key: str):
        response = self.client.renew_listen_key(listenKey=listen_key)
        # logging.info(response)
        return response

    @client_error_handler
    def get_time_request(self) -> Any | dict[Any, Any]:
        response = self.client.time()
        # logging.info(response)
        return response

    @client_error_handler
    def get_orders_request(self, symbol):
        response = self.client.get_orders(symbol=symbol)
        # logging.info(response)
        return response

    @client_error_handler
    def get_balance_request(self):
        response = self.client.balance()
        # logging.info(response)
        return response

    @client_error_handler
    def get_depth_request(self, symbol: str, limit: int = 5):
        response = self.client.depth(symbol=symbol, **{"limit": limit})
        # logging.info(response)
        return OrderBook(**response)

    @client_error_handler
    def change_initial_leverage_request(self, symbol: str, leverage: int) -> ChangeInitialLeverage:
        response = self.client.change_leverage(symbol=symbol, leverage=leverage)
        # logging.info(response)
        return ChangeInitialLeverage(**response)

    @client_error_handler
    def cancel_order(self, symbol: str, orderId: int) -> Any | dict[Any, Any]:
        response = self.client.cancel_order(symbol, orderId)
        # logging.info(response)
        return response

    @client_error_handler
    def book_ticker(self, symbol: str) -> Any | dict[Any, Any]:
        response = self.client.book_ticker(symbol)
        # logging.info(response)
        return response
