"""Message functions for the checks module.

This module provides functions that return error messages for the checks module.

Available functions:

- must_be: Return a list of errors for a missing or incorrect option value.
- refer_to_missing_field: Return a list of errors for a missing field."""

from django.core import checks
from django.db import models

from django_rubble.utils.model_helpers import get_model_label


def must_be(
    type_description: str, option: str, obj: object, error_id: str
) -> list[checks.Error]:
    """Return a list of errors for a missing or incorrect option value.

    Examples:
        >>> must_be("a list", "natural_key_fields", cls, "rubble.E002")
        [Error: The value of 'natural_key_fields' must be a list.]

    Args:
        type_description (str): The description of the required type.
        option (str): The name of the option.
        obj (object): The object to which the option belongs.
        error_id (str): The error ID.

    Returns:
        list[Error]: A list of errors
    """
    return [
        checks.Error(
            f"The value of '{option}' must be {type_description}.",
            obj=obj.__class__,
            id=error_id,
        ),
    ]


def refer_to_missing_field(
    field_name: str, option: str, obj: type[models.Model], error_id: str
) -> list[checks.Error]:
    """Return a list of errors for a missing field.

    Examples:
        >>> refer_to_missing_field("foo", "bar", MyModel, "rubble.E003")
        [Error: The value of 'bar' refers to 'foo', which is not a field of 'MyModel'.]

    Args:
        field_name (str): The name of the missing field.
        option (str): The name of the option.
        obj (type[models.Model]): The model to which the option belongs.
        error_id (str): The error ID.

    Returns:
        list[Error]: A list of errors
    """
    return [
        checks.Error(
            f"The value of '{option}' refers to '{field_name}',"
            f" which is not a field of '{get_model_label(obj)}'.",
            obj=obj,
            id=error_id,
        ),
    ]
