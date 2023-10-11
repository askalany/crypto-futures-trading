# pylint: disable=missing-docstring
from enum import Enum, EnumType, auto

from base.helpers import AutoName


class PriceMatch(Enum):
    # noinspection PyMethodParameters
    def _generate_next_value_(name, start, count, last_values):
        # pylint: disable=no-self-argument
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