from django.contrib import admin


class StampedAdmin(admin.ModelAdmin):
    """A ModelAdmin that sets the created_by and modified_by fields of a StampedModel
    instance to the user that created or modified the instance."""

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)
