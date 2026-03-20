import os
from pathlib import Path

# -----------------------------
# Base directory setup
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

import os

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# -----------------------------
# Security settings
# -----------------------------
SECRET_KEY = 'django-insecure-replace-this-with-random-key'
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# -----------------------------
# Installed apps
# -----------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Project apps
    'users',
    'items',
    'persons',
    'adminpanel',
    'ai_module',
]

# -----------------------------
# Middleware
# -----------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',   # ✅ Required for login sessions
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -----------------------------
# URL & WSGI Configuration
# -----------------------------
ROOT_URLCONF = 'smart_lost_found.urls'
WSGI_APPLICATION = 'smart_lost_found.wsgi.application'

# -----------------------------
# Templates
# -----------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # ✅ You can keep a global "templates" folder for base.html, etc.
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# -----------------------------
# Database (SQLite used for Django internals)
# MongoDB handled manually using PyMongo in views.py
# -----------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# -----------------------------
# Authentication & Password validation
# -----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -----------------------------
# Internationalization
# -----------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'  # ✅ More appropriate for you
USE_I18N = True
USE_TZ = True

# -----------------------------
# Static files
# -----------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# -----------------------------
# Sessions
# -----------------------------
# ✅ Session backend (default file-based) — works well for your project
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 3600  # 1 hour session timeout
SESSION_SAVE_EVERY_REQUEST = True  # Refresh session expiry on activity

# -----------------------------
# Email Configuration
# -----------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # ✅ use the standard backend
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'lostandfounditem25@gmail.com'
EMAIL_HOST_PASSWORD = 'uyokknhdxeogiylg'  # App password
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# -----------------------------
# Default primary key
# -----------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
