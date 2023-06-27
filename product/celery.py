import os
from celery import Celery
from django.conf import settings
from django.core.mail import send_mail

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'product.settings')

app = Celery('product')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def send_email(self, email, url):
    subject = 'New Product Created!'
    html_message = 'Hello there, ' \
                   '<br> Here is the product you created.. ' \
                   '<br> <a href="https://google.com">See Now</a>'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, "", email_from, recipient_list, False, None, None, None, html_message)
