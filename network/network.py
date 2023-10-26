import logging
from typing import Any

from base.Singleton import Singleton
from binance.um_futures import UMFutures
from model import AccountInformation
from model import CancelAllOpenOrders
from model import ChangeInitialLeverage
from network.responses.responses import ListenKeyResponse
from network.responses.responses import MarkPriceResponse
from network.responses.responses import PositionInformationResponse


class BinanceNetworkClient(metaclass=Singleton):
    def __init__(self, client: UMFutures):
        self.client = client

    def cancel_all_orders_request(self, symbol) -> CancelAllOpenOrders:
        response = self.client.cancel_open_orders(symbol=symbol)
        logging.info(response)
        return CancelAllOpenOrders(**response)

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
        response = self.client.new_order(
            symbol=symbol,
            side=side,
            positionSide=position_side,
            type=order_type,
            quantity=str(quantity),
            timeInForce=time_in_force,
            price=price,
        )
        logging.info(response)
        return response

    def new_batch_order_request(self, params) -> Any | dict[Any, Any]:
        response = self.client.new_batch_order(batchOrders=params)
        logging.info(response)
        return response

    def get_position_risk_request(self, symbol: str) -> list[PositionInformationResponse]:
        response = self.client.get_position_risk(symbol=symbol)
        logging.info(response)
        return [PositionInformationResponse(**i) for i in response]

    def get_account_info_request(self) -> AccountInformation:
        response = self.client.account()
        logging.info(response)
        return AccountInformation(**response)

    def get_mark_price_request(self, symbol: str) -> MarkPriceResponse:
        response = self.client.mark_price(symbol=symbol)
        logging.info(response)
        return MarkPriceResponse(**response)

    def get_ticker_price_request(self, symbol: str) -> Any | dict[Any, Any]:
        response = self.client.ticker_price(symbol=symbol)
        logging.info(response)
        return response

    def get_listen_key_request(self) -> ListenKeyResponse:
        response = self.client.new_listen_key()
        logging.info(response)
        return ListenKeyResponse(**response)

    def close_listen_key_request(self, listen_key: str) -> Any | dict[Any, Any]:
        response = self.client.close_listen_key(listenKey=listen_key)
        logging.info(response)
        return response

    def get_open_orders_request(self, symbol: str) -> Any | dict[Any, Any]:
        response = self.client.get_open_orders(symbol=symbol)
        logging.info(response)
        return response

    def keep_alive_request(self, listen_key: str):
        response = self.client.renew_listen_key(listenKey=listen_key)
        logging.info(response)
        return response

    def get_time_request(self) -> Any | dict[Any, Any]:
        response = self.client.time()
        logging.info(response)
        return response

    def get_orders_request(self, symbol):
        response = self.client.get_orders(symbol=symbol)
        logging.info(response)
        return response

    def get_balance_request(self):
        response = self.client.balance()
        logging.info(response)
        return response

    def get_depth_request(self, symbol: str, limit: int = 5):
        response = self.client.depth(symbol=symbol, **{"limit": limit})
        logging.info(response)
        return response

    def change_initial_leverage_request(self, symbol: str, leverage: int) -> ChangeInitialLeverage:
        response = self.client.change_leverage(symbol=symbol, leverage=leverage)
        logging.info(response)
        return ChangeInitialLeverage(**response)
