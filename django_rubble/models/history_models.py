"""Provides history models with enhanced tracking features."""

import copy
from typing import TYPE_CHECKING, Generic, Self, TypeVar

from django.conf import settings
from django.contrib import admin
from django.db import models
from django.db.models.fields.proxy import OrderWrt
from model_utils.fields import StatusField
from simple_history.manager import HistoryManager
from simple_history.models import HistoricalRecords as BaseHistoricalRecords
from simple_history.models import transform_field

from . import override

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser

AUTH_USER_MODEL = getattr(settings, "AUTH_USER_MODEL", "auth.User")

_ModelT = TypeVar("_ModelT", bound=models.Model)


class HistoricalRecords(BaseHistoricalRecords[_ModelT], Generic[_ModelT]):
    """Custom HistoricalRecords to handle StatusField and OrderWrt."""

    @override
    def copy_fields(self, model: models.Model):
        """Add handling for StatusField."""
        fields: dict[str, models.Field] = {}
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


class HistoryModel(models.Model):  # noqa: DJ008
    """Adds useful tracking fields with queryable user fields.

    Fields:
      created_by (ForeignKey): User who created the instance (from history)
      modified_by (ForeignKey): User who last modified the instance (from history)

    Properties:
      created (datetime): history_date from first history record
      modified (datetime): history_date from last history record
    """

    created_by: models.ForeignKey = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.SET_NULL,  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
        null=True,
        blank=True,
        editable=False,
        related_name="+",
        help_text="User who created this instance",
    )
    modified_by: models.ForeignKey = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.SET_NULL,  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
        null=True,
        blank=True,
        editable=False,
        related_name="+",
        help_text="User who last modified this instance",
    )

    history: HistoricalRecords[Self] = HistoricalRecords(
        history_manager=HistoryStampManager, inherit=True
    )

    class Meta:  # noqa: D106
        abstract: bool = True

    @override
    def save(self, *args, **kwargs):
        """Save and update created_by/modified_by from history."""
        # First, save the model so history is created
        super().save(*args, **kwargs)

        # Update tracking fields from history if they're not set
        update_needed = False

        if self.created_by is None:
            first_history = self.history.order_by("history_date").first()
            if first_history and first_history.history_user:
                self.created_by = first_history.history_user
                update_needed = True

        # Always update modified_by from latest history
        last_history = self.history.order_by("-history_date").first()
        if last_history and last_history.history_user:
            if self.modified_by != last_history.history_user:
                self.modified_by = last_history.history_user
                update_needed = True

        # Save again if we updated the tracking fields
        if update_needed:
            # Use update_fields to avoid recursion and additional history entry
            super().save(update_fields=["created_by", "modified_by"])

    @property
    @admin.display
    def created(self):
        return self.history.created().history_date

    @property
    @admin.display
    def modified(self):
        return self.history.modified().history_date
