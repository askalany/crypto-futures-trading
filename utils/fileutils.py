import json

from data.enums import ALL_ENUMS, TIF, PositionSide, Strategy, TickerSymbol
from strategy.TradeStrategy import TradeStrategy
from utils.enumutils import get_enum_member_from_name


def get_inputs_from_file(
    file_name: str = "my_trading.json",
) -> tuple[
    bool,
    bool,
    float,
    TickerSymbol,
    TradeStrategy,
    PositionSide,
    int,
    int,
    TIF,
    float,
    float,
    float,
    float,
]:
    f = open(file_name, "r")
    read = f.read()
    data = json.loads(read)
    once_input = data["once"]
    use_mark_price_input = data["use_mark_price"]
    delay_seconds_input = data["delay_seconds"]
    symbol_input = get_enum_member_from_name(data["symbol"], ALL_ENUMS)
    strategy_input = get_enum_member_from_name(data["strategy"], ALL_ENUMS)
    position_side_input = get_enum_member_from_name(data["position_side"], ALL_ENUMS)
    buy_orders_num_input = data["buy_orders_num"]
    sell_orders_num_input = data["sell_orders_num"]
    tif_input = get_enum_member_from_name(data["tif"], ALL_ENUMS)
    price_sell_max_mult: float = data["price_sell_max_mult"]
    price_sell_min_mult: float = data["price_sell_min_mult"]
    price_buy_max_mult: float = data["price_buy_max_mult"]
    price_buy_min_mult: float = data["price_buy_min_mult"]
    if not isinstance(symbol_input, TickerSymbol):
        raise ValueError("incorrect input for symbol")
    if not isinstance(strategy_input, Strategy):
        raise ValueError("incorrect input for strategy")
    if not isinstance(position_side_input, PositionSide):
        raise ValueError("incorrect input for position_side")
    if not isinstance(tif_input, TIF):
        raise ValueError("incorrect input for tif")
    return (
        once_input,
        use_mark_price_input,
        delay_seconds_input,
        symbol_input,
        strategy_input,
        position_side_input,
        buy_orders_num_input,
        sell_orders_num_input,
        tif_input,
        price_sell_max_mult,
        price_sell_min_mult,
        price_buy_max_mult,
        price_buy_min_mult,
    )
