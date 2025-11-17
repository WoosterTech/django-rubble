

from django.db import models
from django.db.models import QuerySet

SIMPLE_HISTORY_REVERSE_ATTR_NAME = ...
class HistoricalQuerySet(QuerySet):


    def __init__(self, *args, **kwargs) -> None:
        ...

    def as_instances(self) -> HistoricalQuerySet:
        ...

    def filter(self, *args, **kwargs) -> HistoricalQuerySet:
        ...

    def latest_of_each(self) -> HistoricalQuerySet:
        ...



class HistoryManager(models.Manager):
    def __init__(self, model, instance=...) -> None:
        ...

    def get_super_queryset(self):
        ...

    def get_queryset(self):
        ...

    def most_recent(self):
        ...

    def as_of(self, date): # -> HistoricalQuerySet:
        ...

    def bulk_history_create(self, objs, batch_size=..., update=..., default_user=..., default_change_reason=..., default_date=..., custom_historical_attrs=...): # -> None:
        ...



class HistoryDescriptor:
    def __init__(self, model, manager=..., queryset=...) -> None:
        ...

    def __get__(self, instance, owner): # -> Any:
        ...



