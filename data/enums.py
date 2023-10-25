from enum import auto, Enum, EnumType, StrEnum

from base.AutoName import AutoName


# noinspection PyUnusedName,PyUnusedClass
class SymbolType(AutoName):
    FUTURE = auto()


# noinspection PyUnusedName,PyUnusedClass
class ContractType(AutoName):  # contractType
    PERPETUAL = auto()
    CURRENT_MONTH = auto()
    NEXT_MONTH = auto()
    CURRENT_QUARTER = auto()
    NEXT_QUARTER = auto()
    PERPETUAL_DELIVERING = auto()


# noinspection PyUnusedName,PyUnusedClass
class PriceMatch(Enum):  # type
    def _generate_next_value_(name, start, count, last_values):
        # sourcery skip: instance-method-first-arg-name
        return name


# noinspection PyUnusedName,PyUnusedClass
class PriceMatchNone(PriceMatch):
    NONE = auto()


# noinspection PyUnusedName,PyUnusedClass
class PriceMatchOpponent(PriceMatch):
    OPPONENT = auto()
    OPPONENT_5 = auto()
    OPPONENT_10 = auto()
    OPPONENT_20 = auto()


# noinspection PyUnusedName,PyUnusedClass
class PriceMatchQueue(PriceMatch):
    QUEUE = auto()
    QUEUE_5 = auto()
    QUEUE_10 = auto()
    QUEUE_20 = auto()


# noinspection PyUnusedName,PyUnusedClass
class TickerSymbol(AutoName):
    BTCUSDT = auto()
    ETHUSDT = auto()


# noinspection PyUnusedName,PyUnusedClass
class Side(AutoName):
    BUY = auto()
    SELL = auto()


# noinspection PyUnusedName,PyUnusedClass
class Strategy(AutoName):
    FIXED_RANGE = auto()
    PRICE_MATCH_QUEUE = auto()


# noinspection PyUnusedName,PyUnusedClass
class OrderType(AutoName):
    LIMIT = auto()
    MARKET = auto()
    STOP = auto()
    STOP_MARKET = auto()
    TAKE_PROFIT = auto()
    TAKE_PROFIT_MARKET = auto()
    TRAILING_STOP_MARKET = auto()


# noinspection PyUnusedName,PyUnusedClass
class TimeInForce(AutoName):
    GTC = auto()
    IOC = auto()
    FOK = auto()
    GTX = auto()
    GTD = auto()


# noinspection PyUnusedName,PyUnusedClass
class ContractStatus(AutoName):  # (contractStatus，status)
    PENDING_TRADING = auto()
    TRADING = auto()
    PRE_DELIVERING = auto()
    DELIVERING = auto()
    DELIVERED = auto()
    PRE_SETTLE = auto()
    SETTLING = auto()
    CLOSE = auto()


# noinspection PyUnusedName,PyUnusedClass
class OrderStatus(AutoName):
    NEW = auto()
    PARTIALLY_FILLED = auto()
    FILLED = auto()
    CANCELED = auto()
    REJECTED = auto()
    EXPIRED = auto()
    EXPIRED_IN_MATCH = auto()


# noinspection PyUnusedName,PyUnusedClass
class PositionSide(AutoName):
    BOTH = auto()
    LONG = auto()
    SHORT = auto()


# noinspection PyUnusedName,PyUnusedClass
class WorkingType(AutoName):
    MARK_PRICE = auto()
    CONTRACT_PRICE = auto()


# noinspection PyUnusedName,PyUnusedClass
class ResponseType(AutoName):
    ACK = auto()
    RESULT = auto()


# noinspection PyUnusedName,PyUnusedClass
class KlineCandlestickChartIntervals(StrEnum):
    _1m = "1m"
    _3m = "3m"
    _5m = "5m"
    _15m = "15m"
    _30m = "30m"
    _1h = "1h"
    _2h = "2h"
    _4h = "4h"
    _6h = "6h"
    _8h = "8h"
    _12h = "12h"
    _1d = "1d"
    _3d = "3d"
    _1w = "1w"
    _1M = "1M"


# noinspection PyUnusedName,PyUnusedClass
class STPMODE(AutoName):
    NONE = auto()
    EXPIRE_TAKER = auto()
    EXPIRE_BOTH = auto()
    EXPIRE_MAKER = auto()


# noinspection PyUnusedName,PyUnusedClass
class RateLimiters(AutoName):
    REQUEST_WEIGHT = auto()


# noinspection PyUnusedName,PyUnusedClass
class RateLimitIntervals(AutoName):
    MINUTE = auto()


# noinspection PyUnusedName,PyUnusedClass
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
    TimeInForce,
]
