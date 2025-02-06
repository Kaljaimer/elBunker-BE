from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from rest_framework.authtoken.models import Token as DefaultToken

class ExpiringToken(DefaultToken):
    expires = models.DateTimeField(null=True, blank=True)

    def is_expired(self):
        if self.expires is None:
            return False
        return self.expires < timezone.now()

    def save(self, *args, **kwargs):
        if not self.expires:
            self.expires = timezone.now() + timedelta(hours=24)  # Set expiration to 24 hours
        super().save(*args, **kwargs)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    # Add any additional fields you want for your user model

    def __str__(self):
        return f"{self.name} {self.lastname}"

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

class CheckIn(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.check_in_time}"
