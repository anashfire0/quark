from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
# Create your models here.


class CustomUserManager(UserManager):
    pass


class CustomUser(AbstractUser):
    objects = CustomUserManager()

    def __str__(self):
        return f'{self.username} - {self.get_full_name()}' if self.get_full_name() else f'{self.username}'

    def has_profile(self):
        return hasattr(self, 'profile')


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField('Profile picture',
        upload_to='profile_pic',default='profile_pic/default_user.png', blank=True)
    phone_no = models.CharField(max_length=17) # validators should be a list
    def __str__(self):
        return f'{self.user.get_full_name()} - profile'