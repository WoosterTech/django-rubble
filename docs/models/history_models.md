# History Models

::: django_rubble.models.history_models.HistoryModel

## Migration Guide

If you're upgrading from an earlier version where `created_by` and `modified_by` were properties, you'll need to create migrations to add the new database fields:

```python
# After updating django-rubble, run:
python manage.py makemigrations
python manage.py migrate
```

The new fields are nullable and will be automatically populated from the historical records on the next save.

## Usage Example

```python
from django.db import models
from django_rubble.models.history_models import HistoryModel

class Article(HistoryModel):
    title = models.CharField(max_length=200)
    content = models.TextField()

# Now you can query by created_by and modified_by
recent_articles = Article.objects.filter(
    created_by=some_user
).order_by('-created')

modified_by_admin = Article.objects.filter(
    modified_by__is_staff=True
)
```

## Admin Integration

Use the provided `HistoryAdmin` to automatically display the tracking fields as read-only:

```python
from django.contrib import admin
from django_rubble.admin import HistoryAdmin
from .models import Article

@admin.register(Article)
class ArticleAdmin(HistoryAdmin):
    list_display = ['title', 'created_by', 'created', 'modified_by', 'modified']
```
