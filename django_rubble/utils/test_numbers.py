from decimal import Decimal

import pytest

from django_rubble.utils.numbers import is_number, trim_trailing_zeros


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
def test_is_number(number, expected):
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
def test_trim_trailing_zeros(value, expected):
    assert trim_trailing_zeros(value) == expected
    assert Decimal(str(value)).normalize() == expected
