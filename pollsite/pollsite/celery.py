import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pollsite.settings')

app = Celery('pollsite')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update({
    'task_routes': {
        'send_mail': {'queue': 'feeds'}
    }})
# Load task modules from all registered Django app configs.fhd
app.autodiscover_tasks()