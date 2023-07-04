import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'product.settings')

app = Celery('django_celery')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
app.conf.timezone = 'Asia/Kolkata'

app.conf.beat_schedule = {
    # Scheduler Name
    'send-email-every-day': {
        # Task Name (Name Specified in Decorator)
        'task': 'send_mail_users_product_count',
        # Schedule - sends email every 15 mins
        'schedule': 15*60,
        # Function Arguments
        # 'args': ("Hello",)
    },
}
