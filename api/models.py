from django.db import models
import uuid
from django.contrib.auth.models import User


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField()
    category = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "products"
        ordering = ['-createdAt']

        def __str__(self) -> str:
            return self.name





