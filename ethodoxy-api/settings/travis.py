from .base import *
ENVIRONMENT_NAME, _ = os.path.splitext(os.path.basename(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'funnshopp.sqlite3',
    }
}
