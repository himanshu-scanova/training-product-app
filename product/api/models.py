from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db import models
import uuid
from django.contrib.auth.models import User
# from product.celery import send_email
from product.tasks import send_email
from django.urls import reverse
from django.contrib.sites.models import Site


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class ProductModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "products"
        ordering = ['-createdAt']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['name'])
        ]

        def __str__(self) -> str:
            return self.name


@receiver(post_save, sender=ProductModel)
def send_email_to_user(sender, instance=None, created=False, **kwargs):
    email = instance.user.email
    url = "http://" + Site.objects.get(id=2).domain + reverse("product-view", args=[instance.id])
    if created and email:
        send_email.delay(email, url)



