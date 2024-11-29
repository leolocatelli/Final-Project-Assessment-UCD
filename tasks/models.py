from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime
from django.utils import timezone

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    @property
    def is_delayed(self):
        # Verifica se a data de vencimento está no passado em comparação com a data atual
        return self.due_date < timezone.now()

    def clean(self):
        # Se due_date for uma string, converte para datetime
        if isinstance(self.due_date, str):  # Se for uma string
            self.due_date = datetime.strptime(self.due_date, '%Y-%m-%d')

        # Verifica se a data não tem fuso horário e aplica o fuso horário padrão
        if self.due_date.tzinfo is None:
            self.due_date = timezone.make_aware(self.due_date, timezone.get_default_timezone())

        # Chama o clean() da classe pai
        super().clean()

    def save(self, *args, **kwargs):
        self.clean()  # Executa as validações
        super().save(*args, **kwargs)  # Chama o método save original

