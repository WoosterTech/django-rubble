"""Widgets for Django models."""

from django.db.models.fields import Field
from django.template.loader import render_to_string
from pydantic import BaseModel


class DetailWidget(BaseModel):
    field_class: type[Field]
    template_name: str

    def render_to_string(self, list_or_queryset):
        tag_dict = {"values": list_or_queryset}
        return render_to_string(self.template_name, context=tag_dict)
