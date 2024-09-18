import copy

from django.contrib import admin
from django.db import models
from django.db.models.fields.proxy import OrderWrt
from model_utils.fields import StatusField
from simple_history.manager import HistoryManager
from simple_history.models import HistoricalRecords as BaseHistoricalRecords
from simple_history.models import transform_field

from . import override


class HistoricalRecords(BaseHistoricalRecords):
    """Custom HistoricalRecords to handle StatusField and OrderWrt."""

    @override
    def copy_fields(self, model):
        """Add handling for StatusField."""
        fields = {}
        for og_field in self.fields_included(model):
            field = copy.copy(og_field)
            field.remote_field = copy.copy(field.remote_field)
            if isinstance(field, StatusField):
                field.__class__ = models.CharField  # type: ignore[assignment]
            if isinstance(field, OrderWrt):
                # OrderWrt is a proxy field, switch to a plain IntegerField
                field.__class__ = models.IntegerField  # type: ignore[assignment]
            if isinstance(field, models.ForeignKey):
                old_field = field
                old_swappable = old_field.swappable
                old_field.swappable = False
                try:
                    _name, _path, args, field_args = old_field.deconstruct()
                finally:
                    old_field.swappable = old_swappable
                if getattr(old_field, "one_to_one", False) or isinstance(
                    old_field, models.OneToOneField
                ):
                    FieldType = models.ForeignKey  # noqa: N806
                else:
                    FieldType = type(old_field)  # noqa: N806

                # Remove any excluded kwargs for the field.
                # This is useful when a custom OneToOneField is being used that
                # has a different set of arguments than ForeignKey
                for exclude_arg in self.field_excluded_kwargs(old_field):
                    field_args.pop(exclude_arg, None)

                # If field_args['to'] is 'self' then we have a case where the object
                # has a foreign key to itself. If we pass the historical record's
                # field to = 'self', the foreign key will point to an historical
                # record rather than the base record. We can use old_field.model here.
                if field_args.get("to", None) == "self":
                    field_args["to"] = old_field.model

                # Override certain arguments passed when creating the field
                # so that they work for the historical field.
                field_args.update(
                    db_constraint=False,
                    related_name="+",
                    null=True,
                    blank=True,
                    primary_key=False,
                    db_index=True,
                    serialize=True,
                    unique=False,
                    on_delete=models.DO_NOTHING,
                )
                field = FieldType(*args, **field_args)
                field.name = old_field.name
            else:
                transform_field(field)

            # drop db index
            if field.name in self.no_db_index:
                field.db_index = False

            fields[field.name] = field
        return fields


class HistoryStampManager(HistoryManager):
    def created(self):
        return self.order_by("history_date").first()

    def modified(self):
        return self.order_by("-history_date").first()


class HistoryModel(models.Model):
    """Adds useful tracking fields.

    Properties:
      created_by (str): history_user from first history record
      created (datetime): history_date from first history record
      modified_by (str): history_user from last history record
      modified (datetime): history_date from last history record
    """

    history = HistoricalRecords(history_manager=HistoryStampManager, inherit=True)

    class Meta:
        abstract = True

    @property
    @admin.display
    def created_by(self):
        return self.history.created().history_user

    @property
    @admin.display
    def created(self):
        return self.history.created().history_date

    @property
    @admin.display
    def modified_by(self):
        return self.history.modified().history_user

    @property
    @admin.display
    def modified(self):
        return self.history.modified().history_date
