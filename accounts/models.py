from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Você pode adicionar mais campos específicos ao usuário aqui
    bio = models.TextField(null=True, blank=True)  # Exemplo: Biografia do usuário
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)  # Exemplo: Foto de perfil

    def __str__(self):
        return self.username
