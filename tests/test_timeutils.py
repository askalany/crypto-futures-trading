import pytest
from freezegun import freeze_time
from utils.timeutils import get_date_and_time

# Happy path tests with various realistic test values
@pytest.mark.parametrize("test_id, frozen_time, expected_output", [
    ("happy_path_current_time", "2023-04-01 12:00:00", "01/04/2023 12:00:00"),
    ("happy_path_midnight", "2023-04-01 00:00:00", "01/04/2023 00:00:00"),
    ("happy_path_end_of_day", "2023-04-01 23:59:59", "01/04/2023 23:59:59"),
])
def test_get_date_and_time_happy_path(test_id, frozen_time, expected_output):
    # Arrange
    with freeze_time(frozen_time):
        # Act
        result = get_date_and_time()

        # Assert
        assert result == expected_output

# Edge cases are not applicable as the function does not take any input parameters.

# Error cases are not applicable as the function does not have any error handling and always returns the current time.
