from django.db import models
from users.models import CustomUser
from django.urls import reverse
from django.utils import timezone

# Create your models here.


    #custom model manager
class ReminderManager(models.Manager):

    def recently_timed(self):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute('''
                select user_id, title, slug, text, created_on, timed_on, reminded_count, abs(extract(epoch from (current_timestamp)) - extract(epoch from (timed_on))) as recent
                    from reminder_reminder as rems
                    right join users_customuser as users
                    on rems.user_id=users.id
                    order by recent, timed_on;
                ''')
            result_list=[]
            for row in cursor.fetchall():
                if None in row:
                    continue
                p = self.model(user=CustomUser.objects.get(id=row[0]),title=row[1],slug=row[2], text=row[3], created_on=row[4],
                    timed_on=row[5], reminded_count=row[6])
                p.recent = row[7]
                result_list.append(p)
        return result_list

    def recently_created(self):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute('''
                select user_id, title, slug, text, created_on, timed_on, reminded_count, abs(extract(epoch from (current_timestamp)) - extract(epoch from (created_on))) as recent
                    from reminder_reminder as rems
                    right join users_customuser as users
                    on rems.user_id=users.id
                    order by recent, timed_on;
                ''')
            result_list=[]
            for row in cursor.fetchall():
                if None in row:
                    continue
                p = self.model(user=CustomUser.objects.get(id=row[0]),title=row[1],slug=row[2], text=row[3], created_on=row[4],
                    timed_on=row[5], reminded_count=row[6])
                p.recent = row[7]
                result_list.append(p)
        return result_list

class Reminder(models.Model):

    #custom model manager
    objects = ReminderManager()

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
    reminded_count = models.PositiveIntegerField('Reminded count', default=0)

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

