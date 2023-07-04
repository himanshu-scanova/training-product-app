from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User
import api.models
from django.db.models import Count


@shared_task(name="send_mail")
def send_email(email, url):
    subject = 'New Product Created!'
    html_message = render_to_string("email.html", {"url": url})
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, "", email_from, recipient_list, False, None, None, None, html_message)


@shared_task(name="send_mail_users_product_count")
def send_mail_users_product_count():
    users = User.objects.annotate(num_products=Count("product"))
    for user in users:
        try:
            print(f"{user.username} has {user.num_products} product(s)")
            if user.email and not user.is_staff:
                subject = 'Products Update!'
                message = f"You have {user.num_products} product(s) in total right now!"
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email, ]
                send_mail(subject, message, email_from, recipient_list)
        except api.models.Product.DoesNotExist:
            print("Couldn't query DB")
