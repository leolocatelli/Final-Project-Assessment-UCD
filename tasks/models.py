from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime
from django.utils import timezone
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(default="Descrição padrão")
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,  # Permite que a coluna seja nula
        blank=True  # Campo opcional no formulário
    )

    def __str__(self):
        return self.title

    @property
    def is_delayed(self):
        return self.due_date < timezone.now()

    def clean(self):
        if isinstance(self.due_date, str):
            self.due_date = datetime.strptime(self.due_date, '%Y-%m-%d')
        if self.due_date.tzinfo is None:
            self.due_date = timezone.make_aware(self.due_date, timezone.get_default_timezone())
        super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


