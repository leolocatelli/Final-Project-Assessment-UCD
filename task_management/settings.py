"""
Django settings for task_management project.

This file contains configurations for the Django project, including installed applications,
middleware, database setup, authentication, and static files management.
"""

from pathlib import Path
import os
import dj_database_url  # type: ignore # Database configuration for deployment
from dotenv import load_dotenv  # type: ignore # Load environment variables

# Load .env file
load_dotenv()

# Define the base directory for the project
BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 Security settings
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key')

# ⚠️ Debug mode (should be False in production)
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# 🌍 Allowed hosts for the application
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# 🛠️ Installed applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Project apps
    'accounts',
    'tasks',

    # Third-party apps
    'widget_tweaks',
]

# 🔄 Middleware configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve static files efficiently
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 🔗 URL configuration
ROOT_URLCONF = 'task_management.urls'

# 🎨 Template configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "task_management/templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 🔥 WSGI application entry point
WSGI_APPLICATION = 'task_management.wsgi.application'

# 🛢️ Database configuration (Render or local development)
DATABASE_URL = os.getenv('DATABASE_URL', 'postgres://taskuser:task-password@localhost:5432/task_management')
DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}


# 🔑 Password validation settings
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 🌍 Internationalization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 🖼️ Static and media files configuration
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "task_management/static"]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# WhiteNoise configuration for serving static files in production
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# 🔐 Authentication settings
AUTH_USER_MODEL = 'accounts.CustomUser'

# 🔄 Login and logout redirection
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# 📧 Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = f"Task Management App <{EMAIL_HOST_USER}>"
SERVER_EMAIL = EMAIL_HOST_USER

# 📌 Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
    },
}
