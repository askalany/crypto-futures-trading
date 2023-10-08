from enum import Enum
from typing import Any

from binance.um_futures import UMFutures
from requests.adapters import HTTPAdapter

from consts import BASE_URL, KEY, SECRET
from enums import (
    TIF,
    OrderType,
    PositionSide,
    PriceMatch,
    PriceMatchNone,
    Side,
    TickerSymbol,
)
from network import BinanceNetworkClient


class TradeRepo:
    def __init__(self):
        um_client = UMFutures(key=KEY, secret=SECRET, base_url=BASE_URL)
        adapter = HTTPAdapter(pool_connections=200, pool_maxsize=200)
        um_client.session.mount("https://", adapter)
        self.client = BinanceNetworkClient(client=um_client)

    def get_hedge_position_amount(self, symbol: TickerSymbol) -> float:
        return float(
            self.client.get_position_risk_request(symbol=symbol.name)[0]["positionAmt"]
        )

    def get_position_entry_price(self, symbol: TickerSymbol) -> float:
        return float(
            self.client.get_position_risk_request(symbol=symbol.name)[0]["entryPrice"]
        )

    def get_position_unrealized_profit(self, symbol: TickerSymbol) -> float:
        return float(
            self.client.get_position_risk_request(symbol=symbol.name)[0][
                "unRealizedProfit"
            ]
        )

    def get_available_balance(
        self,
    ) -> float:
        return float(self.client.get_account_info_request()["availableBalance"])

    def get_mark_price(self, symbol: TickerSymbol) -> float:
        return float(
            self.client.get_mark_price_request(symbol=symbol.name)["markPrice"]
        )

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

    def get_leverage(self, symbol: TickerSymbol) -> int:
        return int(self.client.get_leverage_request(symbol=symbol.name)[0]["leverage"])

    def cancel_all_orders(self, symbol: TickerSymbol) -> Any | dict[Any, Any]:
        return self.client.cancel_all_orders_request(symbol=symbol.name)

    def get_listen_key(
        self,
    ) -> str:
        return self.client.get_listen_key_request()["listenKey"]

    def close_listen_key(self, listen_key: str) -> Any | dict[Any, Any]:
        return self.client.close_listen_key_request(listen_key=listen_key)

    def get_open_orders(self, symbol: TickerSymbol) -> Any | dict[Any, Any]:
        return self.client.get_open_orders_request(symbol=symbol.name)

    def keep_alive(self, listen_key: str):
        return self.client.keep_alive_request(listen_key=listen_key)

    def get_time(
        self,
    ) -> int:
        return self.client.get_time_request()["serverTime"]
