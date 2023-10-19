import pytest

from data.enums import PositionSide
from utils.mathutils import cost_to_open_position


@pytest.mark.parametrize(
    "quantity, leverage, side, mark_price, order_price, precision, expected_output",
    [
        (1.0, 20, PositionSide.LONG, 9259.84, 9253.30, 2, 462.66),
        (1.0, 20, PositionSide.SHORT, 9259.84, 9253.30, 2, 469.21),
    ],
    ids=["long", "short"],
)
def test_cost_to_open_position_long(
    quantity: float,
    leverage: int,
    side: PositionSide,
    mark_price: float,
    order_price: float,
    expected_output: float,
    precision: int,
):
    result = cost_to_open_position(
        quantity=quantity,
        leverage=leverage,
        mark_price=mark_price,
        order_price=order_price,
        side=side,
        precision=precision,
    )
    # Assert
    assert result == expected_output
