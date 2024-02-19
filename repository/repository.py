import concurrent.futures
from enum import Enum
from typing import Any

from base.Settings import Settings
from base.Singleton import Singleton
from binance.um_futures import UMFutures
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient
from data.enums import OrderType
from data.enums import PositionSide
from data.enums import PriceMatch
from data.enums import PriceMatchNone
from data.enums import Side
from data.enums import TickerSymbol
from data.enums import TimeInForce
from model import AccountInformation
from model import CancelAllOpenOrders
from model import ChangeInitialLeverage
from network.network import BinanceNetworkClient
from network.responses.responses import ListenKeyResponse
from network.responses.responses import MarkPriceResponse
from network.responses.responses import PositionInformationResponse
from requests.adapters import HTTPAdapter


class TradeRepo(metaclass=Singleton):
    def __init__(self, testnet=True):
        key = Settings().KEY
        secret = Settings().SECRET
        um_client = UMFutures(key=key, secret=secret, base_url=Settings().BASE_URL) if testnet else UMFutures()
        adapter = HTTPAdapter(pool_connections=200, pool_maxsize=200)
        um_client.session.mount("https://", adapter)
        self.client = BinanceNetworkClient(client=um_client)

    def get_account_info(self) -> AccountInformation:
        return self.client.get_account_info_request()

    def get_cross_wallet_balance(self) -> float:
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
        time_in_force: TimeInForce = TimeInForce.GTC,
        price_match: PriceMatch = PriceMatchNone.NONE,
    ) -> Any | dict[Any, Any]:
        if time_in_force == TimeInForce.GTX and side == Side.BUY:
            time_in_force = TimeInForce.GTC
        return (
            (
                self.client.new_order_request(
                    symbol=symbol.name,
                    side=side.name,
                    quantity=quantity,
                    position_side=position_side.name,
                    order_type=order_type.name,
                )
                if order_type == OrderType.MARKET
                else self.client.new_order_request(
                    symbol=symbol.name,
                    side=side.name,
                    quantity=quantity,
                    position_side=position_side.name,
                    order_type=order_type.name,
                    price=price,
                    time_in_force=time_in_force.name,
                )
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
                    new_dict[key] = key_value
            new_orders.append(new_dict)
            print(new_orders)
        return self.client.new_batch_order_request(params=new_orders)

    def cancel_all_orders(self, symbol: TickerSymbol) -> CancelAllOpenOrders:
        return self.client.cancel_all_orders_request(symbol=symbol.name)

    def get_listen_key(self) -> ListenKeyResponse:
        return self.client.get_listen_key_request()

    def close_listen_key(self, listen_key: str) -> Any | dict[Any, Any]:
        return self.client.close_listen_key_request(listen_key=listen_key)

    def get_open_orders(self, symbol: TickerSymbol) -> Any | dict[Any, Any]:
        return self.client.get_orders_request(symbol=symbol.name)

    def keep_alive(self, listen_key: str):
        return self.client.keep_alive_request(listen_key=listen_key)

    def get_time(self) -> int:
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
            stream_url=Settings().STREAM_URL,
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
        return list(
            filter(
                lambda x: x.symbol == symbol.name and x.positionSide == Settings().file_input.position_side,
                self.client.get_position_risk_request(symbol=symbol.name),
            )
        )[0]

    def change_initial_leverage(self, symbol: TickerSymbol, leverage: int) -> ChangeInitialLeverage:
        return self.client.change_initial_leverage_request(symbol.name, leverage)

    def get_margin_ratio(self) -> float:
        account_info = self.get_account_info()
        maintenance_margin = account_info.totalMaintMargin
        total_wallet_balance = account_info.totalWalletBalance
        return maintenance_margin / total_wallet_balance

    def get_all_orders(self, symbol: TickerSymbol, side: Side = None):
        orders = self.client.get_orders_request(symbol.name)
        return orders if side is None else list(filter(lambda x: x["side"] == side.name, orders))

    def delete_all_side_orders(self, symbol: TickerSymbol, side: Side):
        all_sell_orders = self.get_all_orders(symbol, Side.SELL)
        all_sell_orders_ids = [order["orderId"] for order in all_sell_orders]

        def cancel_order(orderId: int) -> None:
            response = self.client.cancel_order(symbol.name, orderId)

        with concurrent.futures.ThreadPoolExecutor(max_workers=61) as executor:
            executor.map(cancel_order, all_sell_orders_ids, chunksize=5)
