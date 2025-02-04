from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    # Add any additional fields you want for your user model

    def __str__(self):
        return self.username

class UserLogin(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"
