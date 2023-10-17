from enum import Enum
from typing import Any

from binance.um_futures import UMFutures
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient
from requests.adapters import HTTPAdapter

from base.consts import BASE_URL, KEY, SECRET, STREAM_URL
from base.helpers import Singleton
from data.enums import (
    TIF,
    OrderType,
    PositionSide,
    PriceMatch,
    PriceMatchNone,
    Side,
    TickerSymbol,
)
from network.network import BinanceNetworkClient
from network.responses.responses import (
    AccountInfoResponse,
    CancelAllOrdersResponse,
    ListenKeyResponse,
    MarkPriceResponse,
    PositionInformationResponse,
)


class TradeRepo(metaclass=Singleton):
    def __init__(self):
        um_client = UMFutures(key=KEY, secret=SECRET, base_url=BASE_URL)
        adapter = HTTPAdapter(pool_connections=200, pool_maxsize=200)
        um_client.session.mount("https://", adapter)
        self.client = BinanceNetworkClient(client=um_client)

    def get_account_info(
        self,
    ) -> AccountInfoResponse:
        return self.client.get_account_info_request()

    def get_cross_wallet_balance(
        self,
    ) -> float:
        return self.client.get_balance_request()[0]["crossWalletBalance"]

    def get_mark_price(self, symbol: TickerSymbol) -> MarkPriceResponse:
        return self.client.get_mark_price_request(symbol=symbol.name)

    def get_ticker_price(self, symbol: TickerSymbol) -> float:
        return float(self.client.get_ticker_price_request(symbol=symbol.name)["price"])

    def new_order(
        self,
        symbol: TickerSymbol,
        side: Side,
        quantity: float,
        position_side: PositionSide,
        price: float = -1.0,
        order_type: OrderType = OrderType.LIMIT,
        time_in_force: TIF = TIF.GTC,
        price_match: PriceMatch = PriceMatchNone.NONE,
    ) -> Any | dict[Any, Any]:
        return (
            self.client.new_order_request(
                symbol=symbol.name,
                side=side.name,
                quantity=quantity,
                position_side=position_side.name,
                price=price,
                order_type=order_type.name,
                time_in_force=time_in_force.name,
            )
            if price_match is PriceMatchNone.NONE
            else self.client.new_price_match_order_request(
                symbol=symbol.name,
                side=side.name,
                quantity=quantity,
                position_side=position_side.name,
                order_type=order_type.name,
                time_in_force=time_in_force.name,
                price_match=price_match.name,
            )
        )

    def new_batch_order(self, orders: list) -> Any | dict[Any, Any]:
        new_orders = []
        for order in orders:
            new_dict = {}
            for key in order:
                key_value = order[key]
                if isinstance(key_value, Enum):
                    new_dict[key] = key_value.value
                else:
                    new_dict[key] = str(key_value)
            new_orders.append(new_dict)
        return self.client.new_batch_order_request(params=new_orders)

    def cancel_all_orders(self, symbol: TickerSymbol) -> CancelAllOrdersResponse:
        return self.client.cancel_all_orders_request(symbol=symbol.name)

    def get_listen_key(
        self,
    ) -> ListenKeyResponse:
        return self.client.get_listen_key_request()

    def close_listen_key(self, listen_key: str) -> Any | dict[Any, Any]:
        return self.client.close_listen_key_request(listen_key=listen_key)

    def get_open_orders(self, symbol: TickerSymbol) -> Any | dict[Any, Any]:
        return self.client.get_orders_request(symbol=symbol.name)

    def keep_alive(self, listen_key: str):
        return self.client.keep_alive_request(listen_key=listen_key)

    def get_time(
        self,
    ) -> int:
        return self.client.get_time_request()["serverTime"]

    def get_websocket_client(
        self,
        message_handler,
        on_open=None,
        on_close=None,
        on_error=None,
        on_ping=None,
        on_pong=None,
        is_combined: bool = False,
    ):
        return UMFuturesWebsocketClient(
            stream_url=STREAM_URL,
            on_message=message_handler,
            on_open=on_open,
            on_close=on_close,
            on_error=on_error,
            on_ping=on_ping,
            on_pong=on_pong,
            is_combined=is_combined,
        )

    def get_depth(self, symbol: TickerSymbol, limit: int = 5):
        return self.client.get_depth_request(symbol=symbol.name, limit=limit)

    def get_position_risk(self, symbol: TickerSymbol) -> PositionInformationResponse:
        return self.client.get_position_risk_request(symbol=symbol.name)[0]
