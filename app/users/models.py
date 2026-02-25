from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        CUSTOMER = "CUSTOMER", "Xaridor"
        SELLER = "SELLER", "Sotuvchi"

    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    phone_number = models.CharField(
        max_length=13,
        blank=True,
    )
    role = models.CharField(
        max_length=8,
        choices=Role.choices,
        default=Role.CUSTOMER
    )
    avatar = models.ImageField(upload_to="avatars/", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} | {self.role}"