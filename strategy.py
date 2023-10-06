from enums import TIF, PositionSide, PriceMatchQueue, Side, TickerSymbol
from utils import create_multiple_orders, create_order, get_orders_quantities_and_prices


from typing import Any


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
    buy_low_price = center_price * (1.0 - 0.5)
    sell_high_price = center_price * (1.0 + 0.2)
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
