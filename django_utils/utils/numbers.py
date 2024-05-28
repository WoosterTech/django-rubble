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


def ratio_to_whole(ratio: Decimal | float | str) -> Decimal:
    return Decimal(str(ratio)) * Decimal("100")


def whole_to_ratio(whole: Decimal | float | str) -> Decimal:
    return Decimal(str(whole)) * Decimal("0.01")


def trim_trailing_zeros(value: float | Decimal | str) -> Decimal:
    """Remove trailing zeros from a decimal value."""
    if isinstance(value, Decimal):
        _, _, exponent = value.as_tuple()
    else:
        _, _, exponent = Decimal(str(value)).as_tuple()

    if not isinstance(exponent, int):
        msg = "Exponent must be an integer"
        raise TypeError(msg)

    if exponent < 0:
        new_str = str(value).rstrip("0")
        return Decimal(new_str)

    return Decimal(value)


def set_zero(value: float | Decimal | str) -> Decimal:
    """Set a value to a true Decimal zero if it is zero."""
    decimal_from_string = Decimal(str(value))

    _, decimal_digits, _ = decimal_from_string.as_tuple()

    if len(decimal_digits) == 1 and decimal_digits[0] == 0:
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
