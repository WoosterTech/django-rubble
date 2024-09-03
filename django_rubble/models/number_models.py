from itertools import chain

from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.utils.translation import gettext_lazy as _
from loguru import logger
from pydantic import BaseModel

from django_rubble.checks.messages import must_be, refer_to_missing_field


class SerialNumberConfig(BaseModel):
    """Configuration for NumberModel numbering.

    Example:
        `SerialNumberConfig(prefix="INV", width=4, initial_value=1, step=1)` ->
        `INV0001`, `INV0002`, etc.

    Attributes:
        name: The name of the model, used for NamedSerialNumber.
        initial_value: The starting value for the serial number.
        step: The increment value for the serial number.
        prefix: The prefix for the serial number."""

    name: str | None = None
    initial_value: int = 1
    step: int = 1
    prefix: str
    width: int


class NaturalKeyModelManager(models.Manager):
    def get_by_natural_key(self, *args, **kwargs):
        return self.get(*args, **kwargs)


class NaturalKeyModel(models.Model):
    """Abstract model that adds a `natural_key` method to the model.

    Attributes:
        natural_key_fields: A list of field names that make up the natural key."""

    natural_key_fields: list[str]

    objects = NaturalKeyModelManager()

    class Meta:
        abstract = True

    @classmethod
    def check(cls, **kwargs):
        errors = super().check(**kwargs)

        errors.extend(cls._check_natural_key_fields(**kwargs))

        return errors

    @classmethod
    def _check_natural_key_fields(cls, **kwargs):
        """Check that the natural key fields are set."""
        if not hasattr(cls, "natural_key_fields"):
            return must_be(
                "a list", option="natural_key_fields", obj=cls, error_id="rubble.M002"
            )
        if not isinstance(cls.natural_key_fields, list):
            return must_be(
                "a list", option="natural_key_fields", obj=cls, error_id="rubble.M002"
            )

        return list(
            chain.from_iterable(
                cls._check_natural_key_item(field) for field in cls.natural_key_fields
            )
        )

    @classmethod
    def _check_natural_key_item(cls, field_name: str):
        try:
            _ = cls._meta.get_field(field_name)
        except FieldDoesNotExist:
            return refer_to_missing_field(
                field_name,
                option="natural_key_fields",
                obj=cls,
                error_id="rubble.E001",
            )
        return []

    def natural_key(self):
        return (getattr(self, field_name) for field_name in self.natural_key_fields)


class NamedSerialNumberManager(models.Manager):
    def get_serial_number(
        self,
        parent_model,
        serial_number_config: SerialNumberConfig | None = None,
    ) -> tuple[str, bool]:
        """Generate next serial number, creating NamedSerialModel if one doesn't exist."""  # noqa: E501
        if serial_number_config is None:
            serial_number_config = parent_model.number_config

        model_type = ContentType.objects.get_for_model(parent_model)
        serial_number_config.name = (
            model_type.name
            if serial_number_config.name is None
            else serial_number_config.name
        )

        msg = f"SerialNumberConfig: {serial_number_config}"
        logger.debug(msg)

        named_serial, created = self.get_or_create(
            content_type=model_type,
            defaults={
                "name": serial_number_config.name,
                "next_counter": serial_number_config.initial_value,
                "prefix": serial_number_config.prefix,
                "width": serial_number_config.width,
                "step": serial_number_config.step,
            },
        )
        return named_serial.get_next_number(), created  # type: ignore[attr-defined]


class NamedSerialNumber(models.Model):
    name = models.CharField(_("name"), max_length=50, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    next_counter = models.IntegerField(_("next counter"), default=1)
    step = models.IntegerField(_("step"), default=1)
    prefix = models.CharField(_("prefix"), max_length=10)
    width = models.IntegerField(_("number width"))

    objects = NamedSerialNumberManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "content_type"], name="unique_name_for_content_type"
            )
        ]

    def __str__(self) -> str:
        return f"{self.name} -> next: {self.next_number}"

    @property
    @admin.display
    def next_number(self) -> str:
        return f"{self.prefix}{str(self.next_counter).zfill(self.width)}"

    def get_next_number(self) -> str:
        """Get current formatted number and increment counter."""
        next_number = self.next_number
        self.next_counter += self.step
        self.save()

        return next_number


class NumberedModelManager(models.Manager):
    def get_by_natural_key(self, number: str):
        return self.get(number=number)


class NumberedModel(models.Model):
    """Adds a `number` field that uses `DocumentNumber` to generate values.

    Adds a `natural_key` method to the model, but no manager that uses it.

    Example:

        class Invoice(NumberedModel):
            number_config = SerialNumberConfig(
                    prefix="INV",
                    width=4,
                    initial_value=1,
                    step=1
                )

    Attributes:
        number_config: A SerialNumberConfig instance.
    """

    number = models.CharField(_("number"), unique=True, max_length=10, editable=False)
    number_config: SerialNumberConfig

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        if self._state.adding:
            self.number, _ = NamedSerialNumber.objects.get_serial_number(self)
            msg = f"New number is: {self.number}"
            logger.debug(msg)
        return super().save(*args, **kwargs)

    def natural_key(self):
        return (self.number,)
