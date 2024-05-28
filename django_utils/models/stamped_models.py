from model_utils.models import TimeStampedModel  # type: ignore[import-untyped]

from django_utils.fields.auto_fields import AutoCreatedByField, AutoModifiedByField


class StampedModel(TimeStampedModel):
    """A model that has created_by and modified_by fields that are automatically
    set to the user that created or modified the instance."""

    created_by = AutoCreatedByField()
    modified_by = AutoModifiedByField()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        update_fields = kwargs.get("update_fields", None)
        if update_fields is not None:
            if "modified_by" not in update_fields:
                kwargs["update_fields"] = set(update_fields) | {"modified_by"}

        return super().save(*args, **kwargs)
