from contextlib import nullcontext

import pytest
from django.core.exceptions import ValidationError

from django_rubble.fields.db_fields import CronExpressionField, validate_cron_expression


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("0 1 * * 5", nullcontext(enter_result=None)),
        ("* * 1", pytest.raises(ValidationError)),
    ],
)
def test_cron_validation(value, expected):
    with expected as e:
        assert validate_cron_expression(value) == e


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("0 1 * * 5", nullcontext(enter_result="0 1 * * 5")),
        ("* * 1", pytest.raises(ValidationError)),
    ],
)
def test_cron_field(value, expected):
    field = CronExpressionField()
    with expected as e:
        assert field.clean(value, None) == e
