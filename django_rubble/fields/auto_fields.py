from django.conf import settings
from django.db import models

AUTH_USER_MODEL = getattr(settings, "AUTH_USER_MODEL", "auth.User")


class AutoCreatedByField(models.ForeignKey):
    """A ForeignKey to the user model that is not editable and has a related name
    of '+'.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("editable", False)
        kwargs.setdefault("related_name", "+")
        kwargs.setdefault("to", AUTH_USER_MODEL)
        kwargs.setdefault("on_delete", models.PROTECT)
        super().__init__(*args, **kwargs)


class AutoModifiedByField(models.ForeignKey):
    """A ForeignKey to the user model that is not editable and has a related name
    of '+'.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("editable", False)
        kwargs.setdefault("related_name", "+")
        kwargs.setdefault("to", AUTH_USER_MODEL)
        kwargs.setdefault("on_delete", models.PROTECT)
        super().__init__(*args, **kwargs)
