from enum import StrEnum

from pydantic import BaseModel, Field, model_serializer, model_validator


class Icon(BaseModel):
    """Icon model for use in the application.

    Example:
        `Icon(
            name="pen-fill",
            snippet="<i class='bi bi-pen-fill'></i>",
            toolkit="bootstrap"
        )`
    """

    name: str = Field(description="The name of the icon.")
    snippet: str = Field(default="", description="The HTML snippet for the icon.")
    svg: str = Field(default="", description="The SVG snippet for the icon.")
    toolkit: str | None = Field(default=None, description="The toolkit for the icon.")

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

    Attributes:
        PENCIL: Edit icon.
        TRASH_CAN: Delete icon.
        PLUS_CIRCLE: Create icon.
        ENVELOPE_OPEN: Detail icon.
        LIST_UL: List icon.
        DATABASE_FILL_GEAR: Admin icon.
        CLOCK_HISTORY: History icon.
        ARROWS_COLLAPSE: Expand icon.
        ARROW_CLOCKWISE: Refresh icon.
        CHECK: Check icon.
        X: X icon.
        BOX_ARROW_UP: Check out icon.
        BOX_ARROW_IN_DOWN: Check in icon.
        UPDATE: Edit icon.
        ADMIN: Admin icon.
        DELETE: Delete icon.
        CREATE: Create icon.
        DETAIL: Detail icon.
        LIST: List icon.
        HISTORY: History icon.
        CHECKOUT: Check out icon.
        CHECKIN: Check in icon.
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
    CHECK = '<i class="bi bi-check2-square"></i>'
    X = '<i class="bi bi-x"></i>'
    BOX_ARROW_UP = '<i class="bi bi-box-arrow-up"></i>'
    BOX_ARROW_IN_DOWN = '<i class="bi bi-box-arrow-in-down"></i>'
    CALCULATOR = '<i class="bi bi-calculator"></i>'

    UPDATE = PENCIL
    ADMIN = DATABASE_FILL_GEAR
    DELETE = TRASH_CAN
    CREATE = PLUS_CIRCLE
    DETAIL = ENVELOPE_OPEN
    LIST = LIST_UL
    HISTORY = CLOCK_HISTORY
    CHECKOUT = BOX_ARROW_UP
    CHECKIN = BOX_ARROW_IN_DOWN
