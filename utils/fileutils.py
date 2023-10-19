import json

from base.validation import check_file_inputs
from data.enums import ALL_ENUMS, TimeInForce, PositionSide, Strategy, TickerSymbol
from utils.enumutils import get_enum_member_from_name


def get_inputs_from_file(
    file_name: str = "my_trading.json",
) -> tuple[
    bool,
    bool,
    float,
    TickerSymbol,
    Strategy,
    PositionSide,
    int,
    int,
    TimeInForce,
    float,
    float,
    float,
    float,
]:
    with open(file=file_name, mode="r", encoding="utf-8-sig") as f:
        read = f.read()
        data = json.loads(read)
        once_input = data["once"]
        use_mark_price_input = data["use_mark_price"]
        delay_seconds_input = data["delay_seconds"]
        symbol_input = get_enum_member_from_name(data["symbol"], ALL_ENUMS)
        strategy_input = get_enum_member_from_name(data["strategy"], ALL_ENUMS)
        position_side_input = get_enum_member_from_name(
            data["position_side"], ALL_ENUMS
        )
        buy_orders_num_input = data["buy_orders_num"]
        sell_orders_num_input = data["sell_orders_num"]
        time_in_force_input = get_enum_member_from_name(data["timeInForce"], ALL_ENUMS)
        price_sell_max_mult: float = data["price_sell_max_mult"]
        price_sell_min_mult: float = data["price_sell_min_mult"]
        price_buy_max_mult: float = data["price_buy_max_mult"]
        price_buy_min_mult: float = data["price_buy_min_mult"]
        return check_file_inputs(
            once_input,
            use_mark_price_input,
            delay_seconds_input,
            symbol_input,
            strategy_input,
            position_side_input,
            buy_orders_num_input,
            sell_orders_num_input,
            time_in_force_input,
            price_sell_max_mult,
            price_sell_min_mult,
            price_buy_max_mult,
            price_buy_min_mult,
        )
