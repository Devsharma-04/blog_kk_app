import os
from pathlib import Path
import dj_database_url
# 1. BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Security Settings
SECRET_KEY = 'django-insecure-hhd2p!%eotsk%hqvpdrtj7wl!agu6g_2%9(48o%4)5h$*4*lef'
DEBUG = False  # Production mein False hi rehna chahiye

ALLOWED_HOSTS = ['diagram-chat-app.onrender.com', 'localhost', '127.0.0.1', '*']

# 3. CSRF & Session Fix (Login Error ke liye)
CSRF_TRUSTED_ORIGINS = ['https://diagram-chat-app.onrender.com']
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'None' # Cross-site requests allow karne ke liye

# 4. Application definition
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

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Static files ke liye zaroori
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

# 5. Database (Render ke liye SQLite use kar rahe hain abhi)
DATABASES = {
    'default': dj_database_url.config(
        # Yahan aapko Render se mila hua URL dalna hai
        default="postgresql://daigram_db_user:R945OdsLEPWHCuF1TYjWW8kW7LJuqMin@dpg-d72dmolm5p6s73cvmk7g-a.singapore-postgres.render.com/daigram_db",
        conn_max_age=600
    )
}

# 6. Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# 7. Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 8. Static & Media Files (Fixed)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise Storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 9. Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# 10. PWA SETTINGS
PWA_APP_NAME = 'Diagram'
PWA_APP_DESCRIPTION = "Connect & Explore with Diagram"
PWA_APP_THEME_COLOR = '#007bff'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_START_URL = '/'
PWA_APP_ICONS = [
    {'src': '/static/images/icon-192.png', 'sizes': '192x192'},
    {'src': '/static/images/icon-512.png', 'sizes': '512x512'}
]

# 11. Channels
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}