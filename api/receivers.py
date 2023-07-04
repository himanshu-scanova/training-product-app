from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from api.models import Product
from api.tasks import send_email
from django.urls import reverse
from django.contrib.sites.models import Site


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=Product)
def send_email_to_user(sender, instance=None, created=False, **kwargs):
    email = instance.user.email
    url = "http://" + Site.objects.get(id=3).domain + reverse("product-view", args=[instance.id])
    if created and email:
        send_email.delay(email, url)
