import os
from pathlib import Path

# 1. BASE_DIR hamesha top par hona chahiye
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings
SECRET_KEY = 'django-insecure-hhd2p!%eotsk%hqvpdrtj7wl!agu6g_2%9(48o%4)5h$*4*lef'
DEBUG = False
# Render ka link allow karne ke liye
ALLOWED_HOSTS = ['diagram-chat-app.onrender.com', 'localhost', '127.0.0.1', '*']

# CSRF error fix karne ke liye (Ye sabse zaroori hai)
CSRF_TRUSTED_ORIGINS = [
    'https://diagram-chat-app.onrender.com'
]
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# Static files configuration
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Application definition
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'core',
    'channels',
    'pwa',
]

AUTHENTICATION_BACKENDS=[
    'django.contrib.auth.backends.ModelBackend'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog_kk.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.unread_messages_notifier',

            ],
        },
    },
]

WSGI_APPLICATION = 'blog_kk.wsgi.application'
ASGI_APPLICATION = 'blog_kk.asgi.application'
# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'my_project_db',      # Jo naam Step 1 mein rakha tha
        'USER': 'postgres',           # Default yahi hota hai
        'PASSWORD': '1234', # Jo installation ke waqt rakha tha
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- STATIC FILES CONFIG (FIXED) ---
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- MEDIA FILES CONFIG ---
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# --- PWA SETTINGS ---
PWA_APP_NAME = 'Diagram'
PWA_APP_DESCRIPTION = "Connect & Explore with Diagram"
PWA_APP_THEME_COLOR = '#007bff'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_START_URL = '/'
PWA_APP_ICONS = [
    {
        'src': '/static/images/icon-192.png',
        'sizes': '192x192'
    },
    {
        'src': '/static/images/icon-512.png',
        'sizes': '512x512'
    }
]
PWA_APP_SCREENSHOTS = [
    {
        'src': '/static/images/screenshot-desktop.png',
        'sizes': '1280x720',
        'type': 'image/png',
        'form_factor': 'wide',
        'label': 'Desktop View'
    },
    {
        'src': '/static/images/screenshot-mobile.png',
        'sizes': '720x1280',
        'type': 'image/png',
        # Isme form_factor nahi dalna ya 'narrow' dalna hai
        'label': 'Mobile View'
    }
]
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}