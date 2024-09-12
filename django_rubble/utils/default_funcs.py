"""Useful functions for default values in Django models."""

from datetime import date, datetime

from django.utils import timezone


def django_today() -> date:
    """Return the current date in the timezone of the Django settings.

    Example:
        >>> from django_rubble.utils.default_funcs import django_today
        >>> django_today()
        datetime.date(2021, 1, 1)
    """
    return timezone.now().date()


def django_now() -> datetime:
    """Return the current datetime in the timezone of the Django settings.

    Example:
    >>> from django_rubble.utils.default_funcs import django_now
    >>> django_now()
    datetime.datetime(2021, 1, 1, 0, 0, tzinfo=<UTC>)
    """
    return timezone.now()
