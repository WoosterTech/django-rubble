from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from typing import Any, Generic, TypeAlias, TypeVar

from asgiref.local import Local as LocalContext
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.related_descriptors import (
    ForwardManyToOneDescriptor,
    ForwardOneToOneDescriptor,
    ReverseManyToOneDescriptor,
    ReverseOneToOneDescriptor,
)
from django.utils.functional import cached_property

_ModelT = TypeVar("_ModelT", bound=models.Model)
_FieldT = TypeVar("_FieldT", bound=models.Field)

registered_models = ...

class HistoricalRecords(Generic[_ModelT]):
    DEFAULT_MODEL_NAME_PREFIX: str = "Historical"
    thread: LocalContext = ...
    context: LocalContext = ...
    m2m_models: dict[object, object] = {}

    user_set_verbose_name: str | None = None
    user_set_verbose_name_plural: str | None = None
    user_related_name: str = "+"
    user_db_constraint: bool = True
    table_name: str | None = None
    inherit: bool = False
    history_id_field: str | None = None
    history_change_reason_field: str | None = None
    user_model: type[models.Model] | None = None
    get_user: Callable[..., AbstractBaseUser | None] = ...

    def __init__(
        self,
        verbose_name: str | None = None,
        verbose_name_plural: str | None = None,
        bases: Sequence[type[models.Model]] = ...,
        user_related_name: str = "+",
        table_name: str | None = None,
        inherit: bool = False,
        excluded_fields=...,
        history_id_field: str | None = None,
        history_change_reason_field: str | None = None,
        user_model: type[models.Model] | None = None,
        get_user: Callable[..., AbstractBaseUser | None] = ...,
        cascade_delete_history: bool = False,
        custom_model_name: str | None = None,
        app=...,
        history_user_id_field=...,
        history_user_getter=...,
        history_user_setter=...,
        related_name=...,
        use_base_model_db=...,
        user_db_constraint=...,
        no_db_index=...,
        excluded_field_kwargs=...,
        history_manager=...,
        historical_queryset=...,
        m2m_fields=...,
        m2m_fields_model_field_name=...,
        m2m_bases=...,
    ) -> None: ...
    def contribute_to_class(self, cls, name):  # -> None:
        ...
    def add_extra_methods(self, cls):  # -> None:
        ...
    def finalize(self, sender, **kwargs):  # -> None:
        ...
    def get_history_model_name(self, model):  # -> str | object:
        ...
    def create_history_m2m_model(self, model, through_model):  # -> type[_]:
        ...
    def create_history_model(self, model, inherited):  # -> type[_]:
        ...
    def fields_included(self, model):  # -> list[Any]:
        ...
    def field_excluded_kwargs(self, field): ...
    def copy_fields(self, model):  # -> dict[Any, Any]:
        ...
    def get_extra_fields_m2m(
        self, model, through_model, fields
    ):  # -> dict[str, Any | Callable[..., str] | ForeignKey | UUIDField | AutoField]:
        ...
    def get_extra_fields(
        self, model, fields
    ):  # -> dict[str, Any | UUIDField | AutoField | DateTimeField | TextField | CharField | HistoricalObjectDescriptor | property | Callable[..., Any | str] | Callable[..., str] | staticmethod[..., Any]]:
        ...
    def get_meta_options_m2m(self, through_model):  # -> dict[str, str | object | Any]:
        ...
    def get_meta_options(self, model):  # -> dict[str, tuple[str, str]]:
        ...
    def post_save(self, instance, created, using=..., **kwargs):  # -> None:
        ...
    def post_delete(self, instance, using=..., **kwargs):  # -> None:
        ...
    def pre_delete(self, instance, **kwargs):  # -> None:
        ...
    def get_change_reason_for_object(
        self, instance, history_type, using
    ):  # -> Any | None:
        ...
    def m2m_changed(self, instance, action, attr, pk_set, reverse, **_):  # -> None:
        ...
    def create_historical_record_m2ms(self, history_instance, instance):  # -> None:
        ...
    def create_historical_record(self, instance, history_type, using=...):  # -> None:
        ...
    def get_history_user(self, instance: _ModelT) -> AbstractBaseUser: ...
    def get_m2m_fields_from_model(self, model: models.Model):  # -> list[Any]:
        ...

def transform_field(field: models.Field) -> None: ...

class HistoricDescriptorMixin:
    def get_queryset(self, **hints):  # -> Any:
        ...

class HistoricForwardManyToOneDescriptor(
    HistoricDescriptorMixin, ForwardManyToOneDescriptor
):
    def get_related_model(self): ...

class HistoricReverseManyToOneDescriptor(ReverseManyToOneDescriptor):
    @cached_property
    def related_manager_cls(self):  # -> type[RelatedManager]:
        ...

class HistoricForeignKey(ForeignKey):
    forward_related_accessor_class = HistoricForwardManyToOneDescriptor
    related_accessor_class = HistoricReverseManyToOneDescriptor

class HistoricForwardOneToOneDescriptor(
    HistoricDescriptorMixin, ForwardOneToOneDescriptor
):
    def get_related_model(self): ...

class HistoricReverseOneToOneDescriptor(
    HistoricDescriptorMixin, ReverseOneToOneDescriptor
):
    def get_related_model(self): ...

class HistoricOneToOneField(models.OneToOneField):
    forward_related_accessor_class = HistoricForwardOneToOneDescriptor
    related_accessor_class = HistoricReverseOneToOneDescriptor

def is_historic(instance):  # -> bool:
    ...
def to_historic(instance):  # -> Any | None:
    ...

class HistoricalObjectDescriptor:
    def __init__(self, model, fields_included) -> None: ...
    def __get__(self, instance, owner):  # -> Self:
        ...

class HistoricalChanges(ModelTypeHint):
    def diff_against(
        self,
        old_history: HistoricalChanges,
        excluded_fields: Iterable[str] = ...,
        included_fields: Iterable[str] = ...,
        *,
        foreign_keys_are_objs=...,
    ) -> ModelDelta: ...

@dataclass(frozen=True)
class DeletedObject:
    model: type[models.Model]
    pk: Any

ModelChangeValue: TypeAlias = Any | DeletedObject | list[dict[str, Any | DeletedObject]]

@dataclass(frozen=True)
class ModelChange:
    field: str
    old: ModelChangeValue
    new: ModelChangeValue

@dataclass(frozen=True)
class ModelDelta:
    changes: Sequence[ModelChange]
    changed_fields: Sequence[str]
    old_record: HistoricalChanges
    new_record: HistoricalChanges
