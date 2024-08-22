from enum import StrEnum

from pydantic import BaseModel, model_serializer, model_validator


class Icon(BaseModel):
    name: str
    snippet: str = ""
    svg: str = ""
    toolkit: str | None = None

    def __str__(self) -> str:
        return self.name

    @model_validator(mode="after")
    def check_snippet_or_svg(self):
        assert not (self.snippet == "" and self.svg == "")
        return self

    @model_serializer
    def serialize_model(self):
        if self.has_svg:
            return {"name": self.name, "snippet": self.svg}
        return {"name": self.name, "snippet": self.snippet}

    @property
    def has_snippet(self) -> bool:
        return self.snippet is not None

    @property
    def has_svg(self) -> bool:
        return self.svg is not None

    @property
    def html(self):
        return self.svg if self.has_svg else self.snippet


PENCIL = Icon(
    name="pen-fill", snippet="<i class='bi bi-pen-fill'></i>", toolkit="bootstrap"
)
CLOCK_HISTORY = Icon(
    name="clock-history",
    snippet='<i class="bi bi-clock-history"></i>',
    toolkit="bootstrap",
)
ARROWS_COLLAPSE = Icon(
    name="arrows-collapse",
    snippet='<i class="bi bi-arrows-collapse"></i>',
    toolkit="bootstrap",
)


class LibraryIcon(StrEnum):
    """HTML referencing icon.

    Must include library if required (e.g. for bootstrap/font-awesome/etc.)


    Example include:
    ```
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" />
    ```
    """  # noqa: E501

    PENCIL = PENCIL.snippet
    TRASH_CAN = "<i class='bi bi-trash2'></i>"
    PLUS_CIRCLE = '<i class="bi bi-plus-circle"></i>'
    ENVELOPE_OPEN = '<i class="bi bi-envelope-open"></i>'
    LIST_UL = '<i class="bi bi-list-ul"></i>'
    DATABASE_FILL_GEAR = '<i class="bi bi-database-fill-gear"></i>'
    CLOCK_HISTORY = CLOCK_HISTORY.snippet
    ARROWS_COLLAPSE = ARROWS_COLLAPSE.snippet
    ARROW_CLOCKWISE = '<i class="bi bi-arrow-clockwise"></i>'
    CHECK = '<i class="bi bi-check2-square">'
    X = '<i class="bi bi-x"></i>'
    BOX_ARROW_UP = '<i class="bi bi-box-arrow-up"></i>'
    BOX_ARROW_IN_DOWN = '<i class="bi bi-box-arrow-in-down"></i>'

    UPDATE = PENCIL
    ADMIN = DATABASE_FILL_GEAR
    DELETE = TRASH_CAN
    CREATE = PLUS_CIRCLE
    DETAIL = ENVELOPE_OPEN
    LIST = LIST_UL
    HISTORY = CLOCK_HISTORY
    CHECKOUT = BOX_ARROW_UP
    CHECKIN = BOX_ARROW_IN_DOWN
