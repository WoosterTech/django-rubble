

from typing import Any, Final

from django.db.models import Model
from django.utils.safestring import SafeString

from .models import HistoricalChanges, ModelChange, ModelChangeValue, ModelDelta

def conditional_str(obj: Any) -> str:
    ...

def is_safe_str(s: Any) -> bool:
    ...

class HistoricalRecordContextHelper:


    DEFAULT_MAX_DISPLAYED_DELTA_CHANGE_CHARS: Final = ...
    def __init__(self, model: type[Model], historical_record: HistoricalChanges, *, max_displayed_delta_change_chars=...) -> None:
        ...

    def context_for_delta_changes(self, delta: ModelDelta) -> list[dict[str, Any]]:
        ...

    def format_delta_change(self, change: ModelChange) -> ModelChange:
        ...

    def prepare_delta_change_value(self, change: ModelChange, value: ModelChangeValue) -> Any:
        ...

    def stringify_delta_change_values(self, change: ModelChange, old: Any, new: Any) -> tuple[SafeString, SafeString]:
        ...

    def get_obj_diff_display(self) -> ObjDiffDisplay:
        ...



class ObjDiffDisplay:


    def __init__(self, *, max_length=..., placeholder_len=..., min_begin_len=..., min_end_len=..., min_common_len=...) -> None:
        ...

    def common_shorten_repr(self, *args: Any) -> tuple[str, ...]:
        ...

    def shorten(self, s: str, prefix_len: int, suffix_len: int) -> str:
        ...

    def shortened_str(self, prefix: str, num_skipped_chars: int, suffix: str) -> str:
        ...



