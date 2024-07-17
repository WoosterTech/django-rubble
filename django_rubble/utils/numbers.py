from decimal import Decimal
from typing import Any

from pydantic import BaseModel


def is_number(s: Any):
    """Check if a value can be coerced into a number type."""
    if s is None:
        return False
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True


def any_to_float(s: Any, default: float = 0) -> float:
    """Cast value as float, return default if invalid type."""
    if not is_number(default):
        msg = f"Default must be of type `float` [{default}]"
        raise TypeError(msg)
    try:
        value_float = float(s)
    except ValueError:
        value_float = default

    return value_float


def ratio_to_whole(ratio: Decimal | float | str) -> Decimal:
    """Convert a ratio to a whole number.

    This is useful for converting a ratio to a percentage.

    For example, 0.03 would be converted to 3 (3%).

    Args:
        ratio (Decimal, float, str): The ratio to be converted.

    Returns:
        The whole number. Decimal
    """
    return Decimal(str(ratio)) * Decimal("100")


def whole_to_ratio(whole: Decimal | float | str) -> Decimal:
    """Convert a whole number to a ratio.

    This is useful for converting a percentage to a ratio.

    For example, 3 would be converted to 0.03 (3%).

    Args:
        whole (Decimal, float, str): The whole number to be converted.

    Returns:
        The ratio. Decimal
    """
    return Decimal(str(whole)) * Decimal("0.01")


def trim_trailing_zeros(value: float | Decimal | str) -> Decimal:
    """Remove trailing zeros from a decimal value.

    This is useful for ensuring that a value can be safely compared with another value.

    For example, 3.1400 would be displayed as 3.14.

    Args:
        value (float, Decimal, str): The value to be trimmed.

    Returns:
        The trimmed value. Decimal
    """
    return Decimal(str(value)).normalize()


def set_zero(value: float | Decimal | str) -> Decimal:
    """Set a value to a true Decimal zero if it is zero."""
    decimal_from_string = Decimal(str(value))

    if decimal_from_string == Decimal(0):
        return Decimal()

    return decimal_from_string


class Percent(BaseModel):
    value: Decimal | float | str
    per_hundred: Decimal | float | str | None = None
    decimal_places: int | None = None
    has_decimal_places: bool | None = None

    def model_post_init(self, __context: Any) -> None:
        new_value = trim_trailing_zeros(self.value)
        per_hundred_dec = trim_trailing_zeros(ratio_to_whole(self.value))

        if self.decimal_places is not None:
            new_value = round(new_value, self.decimal_places + 2)
            per_hundred_dec = round(per_hundred_dec, self.decimal_places)
            self.has_decimal_places = True
        else:
            self.has_decimal_places = False

        self.value = set_zero(new_value)
        self.per_hundred = set_zero(per_hundred_dec)

        super().model_post_init(__context)

    @classmethod
    def fromform(cls, val: Decimal, field_decimal_places: int | None = None):
        """Create Percent from human-entry (out of 100)"""
        ratio_decimal = whole_to_ratio(val)
        return cls(value=ratio_decimal, decimal_places=field_decimal_places)

    def __mul__(self, other):
        """Multiply using the ratio (out of 1) instead of human-readable out of 100"""
        return self.value.__mul__(other)

    def __float__(self):
        return float(self.value)

    def as_tuple(self):
        return self.value.as_tuple()

    def is_finite(self):
        return self.value.is_finite()

    def __repr__(self) -> str:
        return f"Percentage('{self.value}', '{self.per_hundred}%')"

    def __str__(self):
        return f"{self.per_hundred}%"
