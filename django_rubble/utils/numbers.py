from decimal import Decimal, DecimalTuple
from typing import Any, TypeVar

from pydantic import BaseModel


def is_number(s: Any) -> bool:
    """Check if a value can be coerced into a number type.

    Examples:
        >>> is_number(10)
        True
        >>> is_number("hello")
        False
        >>> is_number(Decimal("3.14"))
        True

    Args:
        s (Any): The value to check.

    Returns:
        bool: True if the value can be coerced into a number type, False otherwise."""
    if s is None:
        return False
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True


def any_to_float(s: Any, default: float = 0) -> float:
    """Cast value as float, return default if invalid type.

    Examples:
        >>> any_to_float("5.5", 2.3)
        5.5
        >>> any_to_float("test", 0)
        0

    Args:
        s (Any): The value to cast.

    Returns:
        float: The value as a float, or the default if the value is not a number."""
    if not is_number(default):
        msg = f"Default must be of type `float` [{default}]"
        raise TypeError(msg)
    try:
        value_float = float(s)
    except ValueError:
        value_float = default

    return value_float


T = TypeVar("T", int, float, Decimal)


def ratio_to_whole(ratio: T) -> T:
    """Convert a ratio to a whole number.

    This is useful for converting a ratio to a percentage.

    Examples:
        >>> ratio_to_whole(0.03)
        3
        >>> ratio_to_whole(Decimal("1"))
        100

    Args:
        ratio (Decimal, float, str): The ratio to be converted.

    Returns:
        The whole number.
    """
    multiplier = Decimal("100") if isinstance(ratio, Decimal) else 100

    return ratio * multiplier


def whole_to_ratio(whole: T) -> T:
    """Convert a whole number to a ratio.

    This is useful for converting a percentage to a ratio.

    Examples:
        >>> whole_to_ratio(3)
        0.03
        >>> whole_to_ratio(100)
        1

    Args:
        whole (Decimal, float, str): The whole number to be converted.

    Returns:
        The ratio. Decimal
    """
    multiplier = Decimal("100") if isinstance(whole, Decimal) else 100
    return whole / multiplier


def trim_trailing_zeros(value: T) -> Decimal:
    """Remove trailing zeros from a decimal value.

    This is useful for ensuring that a value can be safely compared with another value.

    Examples:
        >>> trim_trailing_zeros(3.1400)
        Decimal('3.14')
        >>> trim_trailing_zeros(Decimal("3.1400"))
        Decimal('3.14')

    Args:
        value (float, Decimal, str): The value to be trimmed.

    Returns:
        The trimmed value. Decimal
    """
    return Decimal(str(value)).normalize()


def set_zero(value: T) -> Decimal:
    """Set a value to a true Decimal zero if it is zero.

    Examples:
        >>> set_zero(0)
        Decimal('0')
        >>> set_zero(0.0)
        Decimal('0')

    Args:
        value (int, float, str): The value to be checked.

    Returns:
        The value as a Decimal if it is zero, otherwise the original value."""
    decimal_from_string = Decimal(str(value))

    if decimal_from_string == Decimal(0):
        return Decimal()

    return decimal_from_string


class Percent(BaseModel):
    """A model for handling percentages.

    This model is designed to handle percentages in a way that is more accurate than
    using floats.

    Attributes:
        value (Decimal, float, str): The value of the percentage.
        per_hundred (Decimal, float, str): The value of the percentage out of 100.
        decimal_places (int): The number of decimal places to use.
        has_decimal_places (bool): Whether the value has decimal places.
    """

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
    def fromform(
        cls, val: Decimal, field_decimal_places: int | None = None
    ) -> "Percent":
        """Create Percent from human-entry (out of 100)

        Examples:
            >>> Percent.fromform(Decimal(3))
            Percent(value=Decimal('0.03'), per_hundred=3)
            >>> Percent.fromform(Decimal("100"))
            Percent(value=Decimal('1'), per_hundred=100)

        Args:
            val (Decimal): The value of the percentage.
            field_decimal_places (int): The number of decimal places to use.

        Returns:
            Percent: The percentage model.
        """
        ratio_decimal = whole_to_ratio(val)
        return cls(value=ratio_decimal, decimal_places=field_decimal_places)

    def __mul__(self, other):
        """Multiply using the ratio (out of 1) instead of human-readable out of 100

        Examples:
            >>> Percent(0.03) * 100
            Decimal('3')
            >>> Percent(1) * 100
            Decimal('100')"""
        return self.value.__mul__(other)

    def __float__(self):
        return float(self.value)

    def as_tuple(self) -> DecimalTuple:
        """Return the value as a decimal tuple.

        Returns:
            DecimalTuple: The value as a decimal tuple."""
        if not isinstance(self.value, Decimal):
            return Decimal(str(self.value)).as_tuple()
        return self.value.as_tuple()

    def is_finite(self):
        return self.value.is_finite()

    def __repr__(self) -> str:
        return f"Percentage('{self.value}', '{self.per_hundred}%')"

    def __str__(self):
        return f"{self.per_hundred}%"
