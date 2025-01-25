from django.contrib.auth.models import AbstractUser
from django.db import models
import os  # Importing necessary modules to access environment variables

class CustomUser(AbstractUser):
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    # def get_profile_picture_url(self):
    #     if self.profile_picture:
    #         return self.profile_picture.url
    #     return '/media/profile_pictures/default_profile.png'

    def get_profile_picture_url(self):
        # Check if the user has a profile picture
        if self.profile_picture:
            # Return the URL of the image stored in S3
            return self.profile_picture.url
        
        # If the user doesn't have a profile picture, return a default image URL from S3
        default_profile_picture_url = f'https://{os.getenv("AWS_STORAGE_BUCKET_NAME")}.s3.amazonaws.com/media/profile_pictures/default_profile.png'
        return default_profile_picture_url

    def __str__(self):
        return self.username