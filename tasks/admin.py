from django.contrib import admin
from .models import Task, Category

# Admin Configuration for Category Model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Configuration for the Category model in the Django Admin interface.
    - Displays the `name` field in the list view.
    - Adds a search bar to filter categories by name.
    """
    list_display = ('name',)  # Fields displayed in the admin list view
    search_fields = ('name',)  # Adds search functionality by category name


# Admin Configuration for Task Model
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Configuration for the Task model in the Django Admin interface.
    - Displays key task attributes in the list view.
    - Provides filters for `completed` status and `category`.
    - Adds search functionality for `title` and `description`.
    """
    list_display = ('title', 'due_date', 'completed', 'category', 'user')  # Key fields shown in the list view
    list_filter = ('completed', 'category')  # Filters for the admin sidebar
    search_fields = ('title', 'description')  # Searchable fields for admin
