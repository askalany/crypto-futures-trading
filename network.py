import logging
from typing import Any

from binance.error import ClientError
from binance.um_futures import UMFutures

from helpers import Singleton


class BinanceNetworkClient(metaclass=Singleton):
    def __init__(self, client: UMFutures):
        self.client = client

    def log_client_error(self, error: ClientError) -> None:
        logging.error(
            f"{error.status_code=}, {error.error_code=}, {error.error_message=}"
        )

    def cancel_all_orders_request(
        self, symbol, receive_window: int = 4000
    ) -> Any | dict[Any, Any]:
        response = {}
        try:
            response = self.client.cancel_open_orders(
                symbol=symbol, recvWindow=receive_window
            )
        except ClientError as error:
            self.log_client_error(error)
        finally:
            return response

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
        response = {}
        try:
            response = self.client.new_order(
                symbol=symbol,
                side=side,
                positionSide=position_side,
                type=order_type,
                quantity=quantity,
                timeInForce=time_in_force,
                priceMatch=price_match,
            )
        except ClientError as error:
            self.log_client_error(error)
        finally:
            return response

    def new_order_request(
        self,
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
            response = self.client.new_order(
                symbol=symbol,
                side=side,
                positionSide=position_side,
                type=order_type,
                quantity=str(quantity),
                timeInForce=time_in_force,
                price=price,
                recvWindow=6000,
            )
        except ClientError as error:
            self.log_client_error(error)
        finally:
            return response

    def new_batch_order_request(self, params) -> Any | dict[Any, Any]:
        response = {}
        try:
            response = self.client.new_batch_order(batchOrders=params)
        except ClientError as error:
            self.log_client_error(error)
        finally:
            return response

    def get_position_risk_request(self, symbol: str) -> Any | dict[Any, Any]:
        response = {}
        try:
            response = self.client.get_position_risk(symbol=symbol, recvWindow=6000)
        except ClientError as error:
            self.log_client_error(error)
        finally:
            return response

    def get_leverage_request(self, symbol: str) -> Any | dict[Any, Any]:
        response = {}
        try:
            response = self.get_position_risk_request(symbol=symbol)
        except ClientError as error:
            self.log_client_error(error)
        finally:
            return response

    def get_account_info_request(
        self,
    ) -> Any | dict[Any, Any]:
        response = {}
        try:
            # noinspection PyCallingNonCallable
            response = self.client.account(recvWindow=6000)
        except ClientError as error:
            self.log_client_error(error)
        finally:
            return response

    def get_mark_price_request(self, symbol: str) -> Any | dict[Any, Any]:
        response = {}
        try:
            response = self.client.mark_price(symbol=symbol)
        except ClientError as error:
            self.log_client_error(error)
        finally:
            return response

    def get_listen_key_request(
        self,
    ) -> Any | dict[Any, Any]:
        response = {}
        try:
            response = self.client.new_listen_key()
        except ClientError as error:
            self.log_client_error(error)
        finally:
            return response

    def close_listen_key_request(self, listen_key: str) -> Any | dict[Any, Any]:
        response = {}
        try:
            response = self.client.close_listen_key(listenKey=listen_key)
        except ClientError as error:
            self.log_client_error(error)
        finally:
            return response

    def get_open_orders_request(self, symbol: str) -> Any | dict[Any, Any]:
        response = {}
        try:
            response = self.client.get_open_orders(symbol=symbol)
        except ClientError as error:
            self.log_client_error(error)
        finally:
            return response

    def keep_alive_request(self, listen_key: str):
        response = {}
        try:
            response = self.client.renew_listen_key(listenKey=listen_key)
        except ClientError as error:
            self.log_client_error(error)
        finally:
            return response

    def get_time_request(self) -> Any | dict[Any, Any]:
        response = {}
        try:
            response = self.client.time()
        except ClientError as error:
            self.log_client_error(error)
        finally:
            return response
    
    def get_orders_request(self,symbol):
        response = {}
        try:
            response =  self.client.get_orders(symbol=symbol)
        except ClientError as error:
            self.log_client_error(error)
        finally:
            return response
