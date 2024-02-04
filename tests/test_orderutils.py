import pytest
from utils.orderutils import create_order
from data.enums import OrderType, PositionSide, PriceMatchNone, Side, TickerSymbol, TimeInForce


# Happy path tests with various realistic test values
@pytest.mark.parametrize(
    "test_id, symbol, side, quantity, position_side, price, order_type, time_in_force, price_match, expected",
    [
        (
            "HP-1",
            TickerSymbol.BTCUSDT,
            Side.BUY,
            1.0,
            PositionSide.LONG,
            50000.0,
            OrderType.LIMIT,
            TimeInForce.GTC,
            PriceMatchNone.NONE,
            {
                "symbol": TickerSymbol.BTCUSDT,
                "side": Side.BUY,
                "type": OrderType.LIMIT,
                "quantity": 1.0,
                "timeInForce": TimeInForce.GTC,
                "positionSide": PositionSide.LONG,
                "price": 50000.0,
            },
        ),
        # Add more happy path test cases here
    ],
)
def test_create_order_happy_path(
    test_id, symbol, side, quantity, position_side, price, order_type, time_in_force, price_match, expected
):
    # Act
    result = create_order(symbol, side, quantity, position_side, price, order_type, time_in_force, price_match)

    # Assert
    assert result == expected


# Edge cases
@pytest.mark.parametrize(
    "test_id, symbol, side, quantity, position_side, price, order_type, time_in_force, price_match, expected",
    [
        (
            "EC-1",
            TickerSymbol.ETHUSDT,
            Side.SELL,
            0.0001,
            PositionSide.SHORT,
            0.0,
            OrderType.MARKET,
            TimeInForce.IOC,
            PriceMatchNone.NONE,
            {
                "symbol": TickerSymbol.ETHUSDT,
                "side": Side.SELL,
                "type": OrderType.MARKET,
                "quantity": 0.0001,
                "timeInForce": TimeInForce.IOC,
                "positionSide": PositionSide.SHORT,
                "price": 0.0,
            },
        ),
        # Add more edge case test cases here
    ],
)
def test_create_order_edge_cases(
    test_id, symbol, side, quantity, position_side, price, order_type, time_in_force, price_match, expected
):
    # Act
    result = create_order(symbol, side, quantity, position_side, price, order_type, time_in_force, price_match)

    # Assert
    assert result == expected


# Error cases
@pytest.mark.parametrize(
    "test_id, symbol, side, quantity, position_side, price, order_type, time_in_force, price_match, exception",
    [
        (
            "ERR-1",
            "INVALID",
            Side.BUY,
            -1.0,
            PositionSide.LONG,
            50000.0,
            OrderType.LIMIT,
            TimeInForce.GTC,
            PriceMatchNone.NONE,
            ValueError,
        ),
        # Add more error case test cases here
    ],
)
def test_create_order_error_cases(
    test_id, symbol, side, quantity, position_side, price, order_type, time_in_force, price_match, exception
):
    # Act & Assert
    with pytest.raises(exception):
        create_order(symbol, side, quantity, position_side, price, order_type, time_in_force, price_match)
