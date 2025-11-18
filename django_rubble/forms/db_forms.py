from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django_rubble.utils.numeric_utils import Percent, is_number


class SimplePercentageField(forms.DecimalField):
    def __init__(
        self,
        *,
        max_value=None,
        min_value=None,
        max_digits=None,
        decimal_places=None,
        **kwargs,
    ):
        if "widget" not in kwargs:
            step = 10 ** (-1 * decimal_places) if decimal_places is not None else 1
            kwargs["widget"] = forms.NumberInput(
                attrs={"class": "percent", "step": step}
            )
        self.max_digits, self.decimal_places = max_digits, decimal_places
        super().__init__(max_value=max_value, min_value=min_value, **kwargs)

    def to_python(self, value):
        val = super().to_python(value)

        if isinstance(val, Percent):
            return val.value

        if is_number(val):
            new_val = Percent.fromform(val)

            return new_val.value

        rtype = type(val)
        raise ValidationError(
            _("Invalid value type: %(rtype)s"),
            code="invalid",
            params={"rtype": rtype},
        )

    def prepare_value(self, value):
        val = super().prepare_value(value)

        if isinstance(val, Percent):
            return val.per_hundred
        if is_number(val):
            if isinstance(val, str):
                new_val = Percent.fromform(val)

                return new_val.per_hundred

            return Percent(value=val).per_hundred

        return val
