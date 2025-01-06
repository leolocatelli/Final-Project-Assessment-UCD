from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime
from django.utils import timezone
from django.conf import settings

# Category Model
class Category(models.Model):
    """
    Represents the task category. Each task can belong to a category for better organization.
    - `name`: The name of the category (e.g., Work, Personal).
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Task Model
class Task(models.Model):
    """
    Represents a task in the application.
    - `title`: Title of the task.
    - `description`: Detailed description of the task.
    - `created_at`: Timestamp of when the task was created.
    - `due_date`: Deadline for the task.
    - `completed`: Status of the task (completed or not).
    - `user`: The user who owns the task.
    - `category`: The category the task belongs to (optional).
    """
    title = models.CharField(max_length=255)
    description = models.TextField(default="Descrição padrão")
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when created
    due_date = models.DateTimeField(default=timezone.now)  # Default due date is now
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Link to the authenticated user
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,  # Category can be removed without deleting the task
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title

    @property
    def is_delayed(self):
        """
        Checks if the task is delayed.
        - A task is delayed if the due date is earlier than the current time.
        """
        return self.due_date < timezone.now()

    def clean(self):
        """
        Custom validation logic for the Task model.
        - Converts string-based dates into datetime objects.
        - Ensures `due_date` is timezone-aware.
        """
        if isinstance(self.due_date, str):  # Handles cases where due_date is passed as a string
            self.due_date = datetime.strptime(self.due_date, '%Y-%m-%d')
        if self.due_date.tzinfo is None:  # Ensures timezone awareness
            self.due_date = timezone.make_aware(self.due_date, timezone.get_default_timezone())
        super().clean()

    def save(self, *args, **kwargs):
        """
        Overrides the default save method.
        - Ensures the `clean` method is called before saving the instance.
        """
        self.clean()  # Validate and process data before saving
        super().save(*args, **kwargs)
