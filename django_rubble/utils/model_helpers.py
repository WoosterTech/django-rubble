from typing import cast

from django.db.models import Model
from django.db.models.fields import Field


def get_model_name(model: type[Model]) -> str:
    """Get model's name as defined in Meta class.

    Will return as all lower case

    Args:
        model: the model to get name from

    Returns:
        model's name
    """
    return model._meta.model_name  # noqa: SLF001


def get_model_verbose_name_plural(model: type[Model]) -> str:
    """Get model's verbose name as defined in Meta class.

    Args:
        model: the model to get verbose name from

    Returns:
        model's verbose name
    """
    return model._meta.verbose_name_plural  # noqa: SLF001


def get_model_label(model: Model) -> str:
    """Get model's label as defined in Meta class.

    Args:
        model: the model to get label from

    Returns:
        model's label"""
    return model._meta.label  # noqa: SLF001


def get_model_fields(
    model: type[Model],
    *,
    fields: list[str] | None = None,
    exclude: list[str] | None = None,
) -> list[Field]:
    """Returns list of fields from model.

    Cannot include both fields and exclude.

    Args:
      model: the model to get fields from
      fields: list of fields to include, default is None
      exclude: list of fields to exclude, default is None

    Returns:
      list of fields
    """
    if fields is not None and exclude is not None:
        msg = "Cannot specify both 'fields' and 'exclude'."
        raise ValueError(msg)

    field_list_full = cast(list[Field], list(model._meta.fields))  # noqa: SLF001  # `_meta` is private

    if fields is not None:
        return [model._meta.get_field(field) for field in fields]  # noqa: SLF001  # `_meta` is private
    if exclude is not None:
        return [field for field in field_list_full if field.name not in exclude]

    return field_list_full
