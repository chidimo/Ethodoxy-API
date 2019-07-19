from .base import *
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(default=DATABASE_URL)
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
