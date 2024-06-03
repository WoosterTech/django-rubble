from datetime import date

from django.utils import timezone


def django_today() -> date:
    """Return the current date in the timezone of the Django settings."""
    return timezone.now().date()
