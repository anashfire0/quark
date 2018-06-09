from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
# Create your models here.

class CustomUserManager(UserManager):
    pass


class CustomUser(AbstractUser):
    class Meta:
        ordering = ['username']
    objects = CustomUserManager()

    def __str__(self):
        return f'{self.username} - {self.get_full_name()}' if self.get_full_name() else f'{self.username}'

    def has_profile(self):
        return hasattr(self, 'profile')


class Profile(models.Model):
    class Meta:
        ordering = ['user']
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField('Profile picture',
        upload_to='profile_pic',default='profile_pic/default_user.png', blank=True)
    phone_no = models.CharField(validators=[RegexValidator(regex = r'^\+?\d{10,12}$', message = 'Invalid phone number')], max_length=17) # validators should be a list
    def __str__(self):
        return f'{self.user.get_full_name()} - profile'