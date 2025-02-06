from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

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
