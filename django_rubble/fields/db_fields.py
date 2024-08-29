from datetime import UTC, datetime

from croniter import croniter
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_rubble.forms.db_forms import (
    SimplePercentageField as SimplePercentageFormField,
)


class SimplePercentageField(models.DecimalField):
    """Enter and display percentages out of 100 but store them out of 1
    in db as decimals

    Because this is based on `models.DecimalField`, `decimal_places` applies to what is
    stored in the db (/1), not what is shown or typed in (/100). With that said, add two
    (2) to whatever is desired in the form for proper validation.
    """

    description = _(
        "percentage (max {max_digits} digits; {decimal_places} decimal places"
    )
    log_name = "models.PercentageField"

    def __init__(
        self,
        verbose_name=None,
        name=None,
        max_digits=None,
        decimal_places=None,
        **kwargs,
    ):
        if decimal_places is not None:
            self.humanize_decimal_places = int(decimal_places) - 2
        else:
            self.humanize_decimal_places = None

        kwargs.update(
            {
                "max_digits": max_digits,
                "decimal_places": decimal_places,
            }
        )

        super().__init__(verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {"form_class": SimplePercentageFormField}
        if self.decimal_places is not None:
            kwargs.update(decimal_places=self.decimal_places - 2)

        defaults.update(kwargs)

        return super().formfield(**defaults)


CRON_REGEX = r"^(\*|([0-5]?[0-9])) (\*|([0-5]?[0-9])) (\*|([01]?[0-9]|2[0-3])) (\*|([01]?[0-9]|2[0-3])) (\*|([0-3]?[0-9])) (\*|([01]?[0-9]|2[0-3])) (\*|([0-5]?[0-9])) (\*|([01]?[0-9]|2[0-3]))$"  # noqa: E501


def validate_cron_expression(value):
    try:
        _ = croniter(value, datetime.now(tz=UTC))
    except (ValueError, KeyError):
        msg = f"{value} is not a valid cron expression."
        raise ValidationError(msg) from None


class CronExpressionField(models.CharField):
    default_validators = [validate_cron_expression]
    description = "A field to store a cron expression"

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = kwargs.get(
            "max_length", 100
        )  # Set max_length to 100 if not provided
        super().__init__(*args, **kwargs)
