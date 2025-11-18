from decimal import Decimal
from typing import TypeVar

import pytest

from django_rubble.utils.numeric_utils import (
    any_to_float,
    is_number,
    ratio_to_whole,
    trim_trailing_zeros,
    whole_to_ratio,
)


@pytest.mark.parametrize(
    ("number", "expected"),
    [
        (10, True),
        (3.14, True),
        ("42", True),
        ("3.14", True),
        ("hello", False),
        (None, False),
    ],
)
def test_is_number(number: int | float | str | None, expected: bool):
    assert is_number(number) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (10, Decimal("10")),
        (3.14, Decimal("3.14")),
        ("42", Decimal("42")),
        ("3.1400", Decimal("3.14")),
    ],
)
def test_trim_trailing_zeros(value: int | float | str, expected: Decimal):
    assert trim_trailing_zeros(value) == expected
    assert Decimal(str(value)).normalize() == expected


@pytest.mark.parametrize(
    ("value", "default", "expected"),
    [
        ("test", 0, 0),
        (5, 0, 5),
        ("5.5", 2.3, 5.5),
    ],
)
def test_value_as_float(value: str | float, default: float, expected: float):
    assert any_to_float(value, default) == expected


def test_any_to_float_exception():
    with pytest.raises(TypeError) as excinfo:
        _ = any_to_float(4.2, "test")  # pyright: ignore[reportArgumentType]
    assert str(excinfo.value) == "Default must be of type `float` [test]"


_T = TypeVar("_T", int, float, Decimal)


@pytest.mark.parametrize(
    ("input_value", "expected"),
    [
        (0.03, 3),
        (Decimal("1"), Decimal("100")),
        (1, 100),
    ],
)
def test_ratio_to_whole(input_value: float | Decimal, expected: float | Decimal):
    assert ratio_to_whole(input_value) == expected


@pytest.mark.parametrize(
    ("input_value", "expected"),
    [
        (3, 0.03),
        (100, 1),
        (Decimal("99"), Decimal("0.99")),
    ],
)
def test_whole_to_ratio(input_value: _T, expected: _T):
    assert whole_to_ratio(input_value) == expected
