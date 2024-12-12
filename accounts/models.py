from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def get_profile_picture_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        return '/media/profile_pictures/default_profile.png'


    def __str__(self):
        return self.username
