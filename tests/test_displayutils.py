import pytest
from display.utils import f_money
from display.utils import f_pct


def test_f_money_positive():
    assert f_money(100) == "[green]100.00[/green]"


def test_f_money_negative():
    assert f_money(-100) == "[red]-100.00[/red]"


def test_f_money_zero():
    assert f_money(0) == "0.00"


def test_f_money_custom_color():
    assert f_money(100, "blue") == "[blue]100.00"


def test_f_money_none_color():
    assert f_money(100, None) == "[green]100.00[/green]"


def test_f_money_large_number():
    assert f_money(1234567890.12345) == "[green]1,234,567,890.12[/green]"


def test_f_money_small_number():
    assert f_money(0.000123) == "[green]0.00[/green]"


def test_f_pct_positive():
    assert f_pct(0.05) == "[green]0.05%[/green]"


def test_f_pct_negative():
    assert f_pct(-0.05) == "[red]-0.05%[/red]"


def test_f_pct_zero():
    assert f_pct(0.0) == "0.00%"


def test_f_pct_large_positive():
    assert f_pct(99.9999) == "[green]100.00%[/green]"


def test_f_pct_large_negative():
    assert f_pct(-99.9999) == "[red]-100.00%[/red]"


def test_f_pct_small_positive():
    assert f_pct(0.0001) == "[green]0.00%[/green]"


def test_f_pct_small_negative():
    assert f_pct(-0.0001) == "[red]-0.00%[/red]"


def test_f_pct_decimals():
    assert f_pct(0.1234567) == "[green]0.12%[/green]"
