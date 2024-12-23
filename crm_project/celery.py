from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set default Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')

app = Celery('crm_project')

# Use Django's settings for configuration
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks automatically
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
