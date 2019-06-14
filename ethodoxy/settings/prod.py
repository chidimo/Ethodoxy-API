from .base import *
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(default=DATABASE_URL)
}

MIDDLEWARE += [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
