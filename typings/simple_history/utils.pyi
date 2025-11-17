

from django.db.models import ManyToManyField

def update_change_reason(instance, reason): # -> None:
    ...

def get_history_manager_for_model(model): # -> Any:
    ...

def get_history_manager_from_history(history_instance): # -> Any:
    ...

def get_history_model_for_model(model): # -> Any:
    ...

def get_app_model_primary_key_name(model):
    ...

def get_m2m_field_name(m2m_field: ManyToManyField) -> str:
    ...

def get_m2m_reverse_field_name(m2m_field: ManyToManyField) -> str:
    ...

def bulk_create_with_history(objs, model, batch_size=..., ignore_conflicts=..., default_user=..., default_change_reason=..., default_date=..., custom_historical_attrs=...): # -> list[Any]:
    ...

def bulk_update_with_history(objs, model, fields, batch_size=..., default_user=..., default_change_reason=..., default_date=..., manager=..., custom_historical_attrs=...): # -> Literal[0]:
    ...

def get_change_reason_from_object(obj): # -> Any | None:
    ...

