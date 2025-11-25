import os

import faker

from .settings import *

faker_gen = faker.Faker(locale='en_US')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'localhost',
        'PORT': int(os.environ.get('POSTGRES_PORT')),
    }
}
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Disable celery
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_BROKER_URL = 'memory://'
CELERY_RESULT_BACKEND = 'cache'
CELERY_CACHE_BACKEND = 'memory'


# Disable logging
LOGGING = {}
