"""Isolated development preview. Never use this module for deployment."""
import os

from .settings import *  # noqa: F403

DEBUG = True
SECRET_KEY = 'local-preview-only-never-use-in-production'
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', 'testserver']
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.preview.sqlite3',
    }
}

# The project's historical migrations contain PostgreSQL-specific SQL.
# syncdb creates only the preview schema directly from the current models.
MIGRATION_MODULES = {name: None for name in ('landing', 'dashboard', 'vouchers', 'analytics')}
MIDDLEWARE = [item for item in MIDDLEWARE if item != 'apps.analytics.middleware.AnalyticsMiddleware']
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'preview@localhost'
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
# Django wraps the default loaders in cached.Loader even with DEBUG enabled.
# Read edited templates on every request while previewing without autoreload.
TEMPLATES = [
    {
        **template,
        'APP_DIRS': False,
        'OPTIONS': {
            **template['OPTIONS'],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    }
    for template in TEMPLATES
]
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
}

# The dashboard has a second psycopg2 connection, independent of DATABASES.
# Block its production defaults even when .env contains Devlink settings.
for key, value in {
    'DEVLINK_DB_HOST': '127.0.0.1',
    'DEVLINK_DB_PORT_INTERNAL': '9',
    'DEVLINK_DB_PORT_EXTERNAL': '9',
    'DEVLINK_DB_NAME': 'preview_disabled',
    'DEVLINK_DB_USER': 'preview_disabled',
    'DEVLINK_DB_PASSWORD': '',
    'DEVLINK_DB_CONNECT_TIMEOUT': '1',
}.items():
    os.environ[key] = value

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'root': {'handlers': ['console'], 'level': 'INFO'},
}
