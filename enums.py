from enum import Enum, auto


# The AutoName class is an enumeration that automatically assigns names to its members based on their
# order.
class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


# The PriceMatch class is an enumeration that represents different types of price matching options.
class PriceMatch(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


# The PriceMatchNone class is a subclass of PriceMatch.
class PriceMatchNone(PriceMatch):
    NONE = auto()


# The PriceMatchOpponent class is a subclass of PriceMatch.
class PriceMatchOpponent(PriceMatch):
    OPPONENT = auto()
    OPPONENT_5 = auto()
    OPPONENT_10 = auto()
    OPPONENT_20 = auto()


# The PriceMatchQueue class is a subclass of PriceMatch.
class PriceMatchQueue(PriceMatch):
    QUEUE = auto()
    QUEUE_5 = auto()
    QUEUE_10 = auto()
    QUEUE_20 = auto()


# The TickerSymbol class is a subclass of AutoName.
class TickerSymbol(AutoName):
    BTCUSDT = auto()


# The Side class is a subclass of AutoName.
class Side(AutoName):
    BUY = auto()
    SELL = auto()


# The PositionSide class is a subclass of AutoName.
class PositionSide(AutoName):
    BOTH = auto()
    LONG = auto()
    SHORT = auto()


# The Strategy class is an enumeration that represents different strategies.
class Strategy(Enum):
    FIXED_RANGE = auto()
    PRICE_MATCH_QUEUE = auto()


# The OrderType class is a subclass of AutoName.
class OrderType(AutoName):
    LIMIT = auto()
    MARKET = auto()
    STOP = auto()
    STOP_MARKET = auto()
    TAKE_PROFIT = auto()
    TAKE_PROFIT_MARKET = auto()
    TRAILING_STOP_MARKET = auto()


# The TIF class is a subclass of AutoName.
class TIF(AutoName):
    GTC = auto()
    IOC = auto()
    FOK = auto()
    GTX = auto()
    GTD = auto()
