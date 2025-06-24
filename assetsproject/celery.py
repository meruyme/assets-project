import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assetsproject.settings')

app = Celery('assetsproject')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.task_default_queue = 'default'

app.autodiscover_tasks()

app.task(bind=True)


def debug_task(self):
    print(f'Request: {self.request!r}')
