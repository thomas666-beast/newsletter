from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsletter_service.settings')

app = Celery('newsletter_service')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(['newsletter'])

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
