from typing import Any
from enums import (
    TIF,
    PositionSide,
    PriceMatchQueue,
    Side,
    Strategy,
    TickerSymbol,
)
from repo import (
    get_available_balance,
    get_hedge_position_amount,
    get_leverage,
    get_mark_price,
    get_position_entry_price,
    new_order,
)
from utils import create_multiple_orders, create_order, get_orders_quantities_and_prices


def work(order) -> Any | dict[Any, Any]:
    if "priceMatch" in order:
        return new_order(
            symbol=order["symbol"],
            side=order["side"],
            quantity=order["quantity"],
            positionSide=order["positionSide"],
            priceMatch=order["priceMatch"],
        )
    else:
        return new_order(
            symbol=order["symbol"],
            side=order["side"],
            quantity=order["quantity"],
            positionSide=order["positionSide"],
            price=order["price"],
        )


def trade(
    strategy: Strategy,
    symbol: TickerSymbol,
    positionSide: PositionSide,
    buy_orders_num: int = 100,
    sell_orders_num: int = 100,
    tif: TIF = TIF.GTC,
) -> list[Any]:
    orders = []
    if strategy is Strategy.FIXED_RANGE:
        center_price = get_position_entry_price(symbol=symbol)
        print(f"{center_price=}")
        if center_price <= 0.0:
            center_price=get_mark_price(symbol=symbol)
        for order in trade_fixed_range(
            symbol=symbol,
            positionSide=positionSide,
            center_price=center_price,
            available_balance=get_available_balance(),
            sell_amount=get_hedge_position_amount(symbol=symbol),
            leverage=get_leverage(symbol),
            tif=tif,
        ):
            orders.append(order)
    else:
        if strategy is Strategy.PRICE_MATCH_QUEUE:
            for order in trade_all_price_match_queue(
                symbol=symbol,
                positionSide=positionSide,
                sell_amount=get_hedge_position_amount(symbol=symbol),
                tif=tif,
            ):
                orders.append(order)
    return orders


def trade_fixed_range(
    symbol: TickerSymbol,
    positionSide: PositionSide,
    center_price: float,
    available_balance: float,
    sell_amount: float,
    leverage: int,
    buy_orders_num: int = 100,
    sell_orders_num: int = 100,
    tif: TIF = TIF.GTC,
) -> list[Any]:
    leveraged_balance = leverage * available_balance
    buy_amount = leveraged_balance / center_price
    buy_high_price = center_price * (1.0 - 0.0009)
    buy_low_price = center_price * (1.0 - 0.2)
    sell_high_price = center_price * (1.0 + 0.5)
    sell_low_price = center_price * (1.0 + 0.0009)
    buy_orders_quantities_and_prices = get_orders_quantities_and_prices(
        orders_num=buy_orders_num,
        high_price=buy_high_price,
        low_price=buy_low_price,
        amount=buy_amount,
    )
    buy_orders = create_multiple_orders(
        symbol=symbol,
        side=Side.BUY,
        quantities_and_prices=buy_orders_quantities_and_prices,
        positionSide=positionSide,
        timeInForce=tif,
    )
    sell_orders_quantities_and_prices = get_orders_quantities_and_prices(
        orders_num=sell_orders_num,
        high_price=sell_high_price,
        low_price=sell_low_price,
        amount=sell_amount,
    )
    sell_orders = create_multiple_orders(
        symbol=symbol,
        side=Side.SELL,
        quantities_and_prices=sell_orders_quantities_and_prices,
        positionSide=positionSide,
        timeInForce=tif,
    )
    orders = buy_orders + sell_orders
    return orders


def trade_all_price_match_queue(
    symbol: TickerSymbol,
    positionSide: PositionSide,
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
        positionSide=positionSide,
        quantity=buy_order_amount,
        priceMatch=PriceMatchQueue.QUEUE,
        timeInForce=tif,
    )
    sell_orders = create_order(
        symbol=symbol,
        side=Side.SELL,
        positionSide=positionSide,
        quantity=sell_order_amount,
        priceMatch=PriceMatchQueue.QUEUE,
        timeInForce=tif,
    )
    orders = [buy_orders] + [sell_orders]
    return orders


def get_max_buy_amount(symbol: TickerSymbol):
    return (get_leverage(symbol=symbol) * get_available_balance()) / get_mark_price(
        symbol=symbol
    )
