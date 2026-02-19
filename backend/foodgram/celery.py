import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodgram.settings')

app = Celery('foodgram')
app.config_from_object('celeryconfig')
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
