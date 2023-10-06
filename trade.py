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
    new_order,
)
from utils import create_multiple_orders, create_order, get_orders_quantities_and_prices


def work(order) -> Any | dict[Any, Any]:
    """
    The function `work` takes an order as input and creates a new order with the same parameters, but
    with a different price depending on whether the "priceMatch" key is present in the order.

    :param order: The `order` parameter is a dictionary that contains the details of an order. It has
    the following keys:
    :return: a new order. If the "priceMatch" key is present in the order dictionary, it will create a
    new order with the "priceMatch" value. Otherwise, it will create a new order with the "price" value.
    """
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
    """
    The `trade` function executes trading orders based on the specified strategy, symbol, position side,
    and other parameters.

    :param strategy: The `strategy` parameter is an enum that represents the trading strategy to be
    used. It can have one of the following values:
    :type strategy: Strategy
    :param symbol: The `symbol` parameter represents the ticker symbol of the asset you want to trade.
    It is typically a string that identifies a specific asset, such as "BTCUSDT" for Bitcoin against
    USDT (Tether)
    :type symbol: TickerSymbol
    :param positionSide: The parameter "positionSide" is used to specify the side of the position you
    want to trade. It can have two possible values: "LONG" or "SHORT". If you want to trade the long
    side of the position, you would pass "LONG" as the value for this parameter. If
    :type positionSide: PositionSide
    :param buy_orders_num: The parameter `buy_orders_num` represents the number of buy orders to be
    placed in the trade, defaults to 100
    :type buy_orders_num: int (optional)
    :param sell_orders_num: The parameter `sell_orders_num` represents the number of sell orders to be
    placed in the `trade` function, defaults to 100
    :type sell_orders_num: int (optional)
    :param tif: The `tif` parameter stands for "Time in Force" and it determines how long an order will
    remain active before it is automatically canceled. It is an optional parameter with a default value
    of `TIF.GTC`, which stands for "Good Till Cancelled". This means that the order will remain
    :type tif: TIF
    :return: a list of orders.
    """
    orders = []
    if strategy is Strategy.FIXED_RANGE:
        for order in trade_fixed_range(
            symbol=symbol,
            positionSide=positionSide,
            mark_price=get_mark_price(symbol=symbol),
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
    mark_price: float,
    available_balance: float,
    sell_amount: float,
    leverage: int,
    buy_orders_num: int = 100,
    sell_orders_num: int = 100,
    tif: TIF = TIF.GTC,
) -> list[Any]:
    """
    The function `trade_fixed_range` creates a list of buy and sell orders for a given symbol, position
    side, mark price, available balance, sell amount, leverage, buy orders number, sell orders number,
    and time in force.

    :param symbol: The symbol parameter represents the ticker symbol of the trading pair you want to
    trade. For example, if you want to trade the BTC/USDT pair, the symbol would be "BTCUSDT"
    :type symbol: TickerSymbol
    :param positionSide: The parameter "positionSide" determines whether the position is long or short.
    It can take two possible values: "PositionSide.LONG" for a long position or "PositionSide.SHORT" for
    a short position
    :type positionSide: PositionSide
    :param mark_price: The mark_price is the current price of the symbol being traded. It is used to
    calculate the buy and sell prices for the orders
    :type mark_price: float
    :param available_balance: The available balance is the amount of funds that you have available for
    trading. It represents the total amount of money that you can use to enter into trades
    :type available_balance: float
    :param sell_amount: The `sell_amount` parameter represents the amount of the asset that you want to
    sell in each sell order
    :type sell_amount: float
    :param leverage: The leverage parameter determines the amount of leverage to use in the trade. It is
    an integer value that represents the leverage ratio. For example, if the leverage is set to 10, it
    means that the trade will be executed with 10 times the available balance
    :type leverage: int
    :param buy_orders_num: The parameter `buy_orders_num` represents the number of buy orders to be
    created, defaults to 100
    :type buy_orders_num: int (optional)
    :param sell_orders_num: sell_orders_num is the number of sell orders to be created. It determines
    how many sell orders will be placed during the trading process, defaults to 100
    :type sell_orders_num: int (optional)
    :param tif: TIF stands for Time in Force, which is an attribute of an order that determines how long
    the order will remain active before it is either executed or cancelled. The default value for TIF in
    the function is set to GTC, which stands for "Good 'Til Cancelled". This means
    :type tif: TIF
    :return: a list of orders.
    """
    leveraged_balance = leverage * available_balance
    buy_amount = leveraged_balance / mark_price
    buy_high_price = mark_price * (1.0 - 0.0014)
    buy_low_price = mark_price * (1.0 - 0.1)
    sell_high_price = mark_price * (1.0 + 0.025)
    sell_low_price = mark_price * (1.0 + 0.0014)
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
    """
    The function `trade_all_price_match_queue` creates a list of buy and sell orders with specified
    quantities and price matching strategy.

    :param symbol: The symbol parameter represents the ticker symbol of the asset you want to trade. It
    could be a stock symbol, cryptocurrency symbol, or any other financial instrument symbol
    :type symbol: TickerSymbol
    :param positionSide: The parameter "positionSide" is used to specify the position side of the order.
    It can have two possible values: "LONG" or "SHORT"
    :type positionSide: PositionSide
    :param sell_amount: The `sell_amount` parameter represents the total amount of the asset that you
    want to sell
    :type sell_amount: float
    :param buy_orders_num: The parameter `buy_orders_num` represents the number of buy orders to be
    created, defaults to 4
    :type buy_orders_num: int (optional)
    :param sell_orders_num: The parameter `sell_orders_num` represents the number of sell orders that
    will be created, defaults to 4
    :type sell_orders_num: int (optional)
    :param tif: The parameter "tif" stands for "Time in Force" and it is an optional parameter with a
    default value of "TIF.GTC". "TIF" is an enumeration that represents different time in force options
    for orders. In this case, "TIF.GTC" stands for "Good
    :type tif: TIF
    :return: a list of orders.
    """
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
    """
    The function calculates the maximum amount that can be bought for a given symbol based on leverage,
    available balance, and mark price.

    :param symbol: The parameter "symbol" is of type TickerSymbol, which represents the symbol of a
    financial instrument such as a stock or cryptocurrency
    :type symbol: TickerSymbol
    :return: the maximum buy amount for a given symbol.
    """
    return (get_leverage(symbol=symbol) * get_available_balance()) / get_mark_price(
        symbol=symbol
    )
