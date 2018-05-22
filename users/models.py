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


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profiles')
    profile_pic = models.ImageField('Profile picture',
        upload_to='profile_pic', blank=True)
    phone_no = models.CharField('Phone No.', max_length=17, blank=True)
    dob = models.DateField('Date Of Birth', blank=True, null=True)

    def __str__(self):
        return f'{self.user.get_full_name()} - profile'