from django.db import models
from users.models import CustomUser
from django.urls import reverse
from django.utils import timezone

# Create your models here.


class Reminder(models.Model):
    class Meta:
        ordering = ['timed_on']
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='reminders')
    title = models.CharField('Title', max_length=256,
                             help_text='Quick summary of your reminder.')
    slug = models.SlugField('Slug', max_length=256)
    text = models.TextField('Text')
    created_on = models.DateTimeField('Created on', auto_now_add=True)
    timed_on = models.DateTimeField('Timed on')
    reminded_count = models.PositiveIntegerField('Reminded count')

    def __str__(self):
        trunc_text = slice(30)
        s = f'{self.user.username} - {self.title} - '
        return s + f'{self.text[trunc_text]}...' if len(self.text) > 50 else s + f'{self.text}'

    def get_absolute_url(self):
        return reverse('reminder:reminder_detail', args=[self.slug])

    def get_update_url(self):
        return reverse('reminder:edit_reminder', args=[self.slug])

    def get_delete_url(self):
        return reverse('reminder:delete_reminder', args=[self.slug])

    def is_expired(self):
        return self.timed_on < timezone.now() 