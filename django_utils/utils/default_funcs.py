from datetime import date

from django.utils import timezone


def django_today() -> date:
    return timezone.now().date()
