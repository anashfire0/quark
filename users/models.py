from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.

class CustomUserManager(UserManager):
    pass

class CustomUser(AbstractUser):
    objects = CustomUserManager()

    def __str__(self):
        return f'{self.username} - {self.get_full_name()}'