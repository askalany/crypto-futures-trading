from enums import (
    PriceMatchOpponent,
    get_enum_member_from_name,
    get_enum_type_from_member_name,
)


def test_get_enum_type_from_member_name():
    assert (
        get_enum_type_from_member_name("PriceMatchOpponent.OPPONENT")
        == PriceMatchOpponent
    )


def test_get_enum_member_from_name():
    assert (
        get_enum_member_from_name("PriceMatchOpponent.OPPONENT")
        == PriceMatchOpponent.OPPONENT
    )
