from utils.enumutils import get_enum_member_from_name
from data.enums import ALL_ENUMS, PriceMatchOpponent
from utils.enumutils import get_enum_type_from_member_name


def test_get_enum_type_from_member_name():
    assert (
        get_enum_type_from_member_name("PriceMatchOpponent.OPPONENT", ALL_ENUMS)
        == PriceMatchOpponent
    )


def test_get_enum_member_from_name():
    assert (
        get_enum_member_from_name("PriceMatchOpponent.OPPONENT", ALL_ENUMS)
        == PriceMatchOpponent.OPPONENT
    )
