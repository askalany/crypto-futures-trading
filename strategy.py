from typing import Any

from rich import print

from enums import TIF, AmountSpacing, PositionSide, PriceMatchQueue, Side, TickerSymbol
from utils import create_all_queue_price_match_orders, get_max_buy_amount
from utils import (
    create_multiple_orders,
    create_order,
    get_grid_maxs_and_mins,
    get_orders_quantities_and_prices,
)


def trade_fixed_range(
    symbol: TickerSymbol,
    position_side: PositionSide,
    center_price: float,
    available_balance: float,
    sell_amount: float,
    leverage: int,
    buy_orders_num: int = 100,
    sell_orders_num: int = 100,
    tif: TIF = TIF.GTC,
) -> list[Any]:
    leveraged_balance = leverage * available_balance
    amount_buy = leveraged_balance / center_price
    price_sell_max_mult = 1.0 + 0.02
    price_sell_min_mult = 1.0 + 0.0009
    price_buy_max_mult = 1.0 - 0.0009
    price_buy_min_mult = 1.0 - 0.2
    (
        price_sell_max,
        price_sell_min,
        price_buy_max,
        price_buy_min,
    ) = get_grid_maxs_and_mins(
        center_price=center_price,
        price_sell_max_mult=price_sell_max_mult,
        price_sell_min_mult=price_sell_min_mult,
        price_buy_max_mult=price_buy_max_mult,
        price_buy_min_mult=price_buy_min_mult,
    )
    print(f"{price_buy_min=}, {price_buy_max=}, {price_sell_min=}, {price_sell_max=}")
    buy_orders_quantities_and_prices = get_orders_quantities_and_prices(
        orders_num=buy_orders_num,
        high_price=price_buy_max,
        low_price=price_buy_min,
        amount=amount_buy,
        order_quantity_min=0.001,
        amount_spacing=AmountSpacing.GEOMETRIC,
    )
    buy_orders = create_multiple_orders(
        symbol=symbol,
        side=Side.BUY,
        quantities_and_prices=buy_orders_quantities_and_prices,
        position_side=position_side,
        time_in_force=tif,
    )
    sell_orders_quantities_and_prices = get_orders_quantities_and_prices(
        orders_num=sell_orders_num,
        high_price=price_sell_max,
        low_price=price_sell_min,
        amount=sell_amount,
        order_quantity_min=0.001,
        amount_spacing=AmountSpacing.GEOMETRIC,
    )
    sell_orders = create_multiple_orders(
        symbol=symbol,
        side=Side.SELL,
        quantities_and_prices=sell_orders_quantities_and_prices,
        position_side=position_side,
        time_in_force=tif,
    )
    orders = buy_orders + sell_orders
    print(f"{len(orders)=}, {len(buy_orders)=}, {len(sell_orders)=}")
    return orders


def trade_all_price_match_queue(
    symbol: TickerSymbol,
    position_side: PositionSide,
    sell_amount: float,
    buy_orders_num: int = 4,
    sell_orders_num: int = 4,
    tif: TIF = TIF.GTC,
) -> list[dict[str, Any]]:
    buy_amount = get_max_buy_amount(symbol)
    buy_order_amount = round(buy_amount / float(buy_orders_num), 4)
    sell_order_amount = round(sell_amount / float(sell_orders_num), 4)
    buy_orders = create_all_queue_price_match_orders(
        symbol=symbol,
        side=Side.BUY,
        position_side=position_side,
        quantity=min(buy_order_amount, 1000.0),
    )
    sell_orders = create_all_queue_price_match_orders(
        symbol=symbol,
        side=Side.SELL,
        position_side=position_side,
        quantity=min(sell_order_amount, 1000.0),
    )
    orders = buy_orders + sell_orders
    return orders
