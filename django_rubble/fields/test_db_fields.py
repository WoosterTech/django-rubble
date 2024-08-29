import pytest

from django_rubble.fields.db_fields import SimplePercentageField
from django_rubble.forms.db_forms import (
    SimplePercentageField as SimplePercentageFormField,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (None, None),  # decimal_places is None
        (2, 0),  # Percent has no decimal places
    ],
)
def test_simple_percentage_field(value: int | None, expected: int | None):
    field = SimplePercentageField(max_digits=3, decimal_places=value)

    assert field.humanize_decimal_places == expected
    assert isinstance(field.formfield(), SimplePercentageFormField)
