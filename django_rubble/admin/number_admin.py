from django.contrib import admin

from django_rubble.models.number_models import NamedSerialNumber


@admin.register(NamedSerialNumber)
class NamedSerialNumberAdmin(admin.ModelAdmin):
    list_display = ["name", "content_type", "next_number"]
    fields = ["name", "content_type", "next_counter", "step", "prefix", "width"]
