import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

# nome igual ao nome do project root
app = Celery('app')

# carrega config do Django que começam com CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# encontra tasks em todos apps registrados
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
