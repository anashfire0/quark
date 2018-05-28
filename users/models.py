from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
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
    phone_regex = RegexValidator(regex=r'^\+?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'.")
    phone_no = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    def __str__(self):
        return f'{self.user.get_full_name()} - profile'