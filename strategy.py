from typing import Any

from rich import print

from enums import TIF, AmountSpacing, PositionSide, PriceMatchQueue, Side, TickerSymbol
from utils import create_multiple_orders, create_order, get_orders_quantities_and_prices


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


def check_grid_maxs_and_mins(
    price_sell_max, price_sell_min, price_buy_max, price_buy_min
) -> None:
    if price_sell_min >= price_sell_max:
        raise Exception("price_sell_min >= price_sell_max")
    if price_buy_max >= price_sell_min:
        raise Exception("price_buy_max >= price_sell_min")
    if price_buy_min >= price_buy_max:
        raise Exception("price_buy_min >= price_buy_max")


def get_grid_maxs_and_mins(
    center_price: float,
    price_sell_max_mult: float,
    price_sell_min_mult: float,
    price_buy_max_mult: float,
    price_buy_min_mult: float,
) -> tuple[float, float, float, float]:
    price_sell_max = center_price * price_sell_max_mult
    price_sell_min = center_price * price_sell_min_mult
    price_buy_max = center_price * price_buy_max_mult
    price_buy_min = center_price * price_buy_min_mult
    check_grid_maxs_and_mins(
        price_sell_max=price_sell_max,
        price_sell_min=price_sell_min,
        price_buy_max=price_buy_max,
        price_buy_min=price_buy_min,
    )
    return price_sell_max, price_sell_min, price_buy_max, price_buy_min


def trade_all_price_match_queue(
    symbol: TickerSymbol,
    position_side: PositionSide,
    sell_amount: float,
    buy_orders_num: int = 4,
    sell_orders_num: int = 4,
    tif: TIF = TIF.GTC,
) -> list[dict[str, Any]]:
    buy_amount = 1.0  # get_max_buy_amount(symbol)
    buy_order_amount = buy_amount / float(buy_orders_num)
    sell_order_amount = sell_amount / float(sell_orders_num)
    buy_orders = create_order(
        symbol=symbol,
        side=Side.BUY,
        position_side=position_side,
        quantity=buy_order_amount,
        price_match=PriceMatchQueue.QUEUE,
        time_in_force=tif,
    )
    sell_orders = create_order(
        symbol=symbol,
        side=Side.SELL,
        position_side=position_side,
        quantity=sell_order_amount,
        price_match=PriceMatchQueue.QUEUE,
        time_in_force=tif,
    )
    orders = [buy_orders] + [sell_orders]
    return orders
