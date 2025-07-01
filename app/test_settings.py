import faker
import os
from .settings import *

faker_gen = faker.Faker(locale='en_US')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'localhost',
        'PORT': int(os.environ.get('POSTGRES_PORT'))
    }
}
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'