"""Useful functions for default values in Django models."""

from datetime import date, datetime

from django.utils import timezone


def django_today() -> date:
    """Return the current date in the timezone of the Django settings."""
    return timezone.now().date()


def django_now() -> datetime:
    """Return the current datetime in the timezone of the Django settings."""
    return timezone.now()
