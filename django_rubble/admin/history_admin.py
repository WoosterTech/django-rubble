from django.contrib import admin  # type: ignore[import-untyped]


class HistoryAdmin(admin.ModelAdmin):
    """A ModelAdmin for HistoryModel instances.

    Automatically adds created_by and modified_by to readonly_fields
    for display in the admin interface.
    """

    readonly_fields = ("created_by", "modified_by", "created", "modified")


class HistoryTabularInline(admin.TabularInline):
    """An InlineModelAdmin for HistoryModel instances.

    Automatically adds created_by and modified_by to readonly_fields
    for display in the admin interface.
    """

    readonly_fields = ("created_by", "modified_by", "created", "modified")
