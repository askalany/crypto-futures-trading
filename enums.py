from enum import Enum, EnumType, auto

from utils import get_enum_class_name


class AutoName(Enum):
    # noinspection PyMethodParameters
    def _generate_next_value_(name, start, count, last_values):
        # sourcery skip: instance-method-first-arg-name
        return name


class PriceMatch(Enum):
    # noinspection PyMethodParameters
    def _generate_next_value_(name, start, count, last_values):
        # sourcery skip: instance-method-first-arg-name
        return name


class PriceMatchNone(PriceMatch):
    NONE = auto()


class PriceMatchOpponent(PriceMatch):
    OPPONENT = auto()
    OPPONENT_5 = auto()
    OPPONENT_10 = auto()
    OPPONENT_20 = auto()


class PriceMatchQueue(PriceMatch):
    QUEUE = auto()
    QUEUE_5 = auto()
    QUEUE_10 = auto()
    QUEUE_20 = auto()


class TickerSymbol(AutoName):
    BTCUSDT = auto()


class Side(AutoName):
    BUY = auto()
    SELL = auto()


class PositionSide(AutoName):
    BOTH = auto()
    LONG = auto()
    SHORT = auto()


class Strategy(Enum):
    FIXED_RANGE = auto()
    PRICE_MATCH_QUEUE = auto()


class OrderType(AutoName):
    LIMIT = auto()
    MARKET = auto()
    STOP = auto()
    STOP_MARKET = auto()
    TAKE_PROFIT = auto()
    TAKE_PROFIT_MARKET = auto()
    TRAILING_STOP_MARKET = auto()


class TIF(AutoName):
    GTC = auto()
    IOC = auto()
    FOK = auto()
    GTX = auto()
    GTD = auto()


class AmountSpacing(Enum):
    LINEAR = auto()
    GEOMETRIC = auto()


ALL_ENUMS: list[EnumType] = [
    PriceMatch,
    PriceMatchNone,
    PriceMatchOpponent,
    PriceMatchQueue,
    TickerSymbol,
    Side,
    PositionSide,
    Strategy,
    OrderType,
    TIF,
]


def get_enum_type_from_member_name(key_str: str) -> EnumType:
    split_string = key_str.split(".")
    for i in ALL_ENUMS:
        if split_string[0] == get_enum_class_name(i):
            return i
    raise ValueError("Invalid enum")


def get_enum_member_from_name(name_str: str) -> EnumType:
    enum_type = get_enum_type_from_member_name(name_str)
    if enum_type is not None:
        for _, member in enum_type.__members__.items():
            if name_str == f"{member}":
                return member
    raise ValueError(f"{name_str} is not a member of {enum_type.__name__}")
