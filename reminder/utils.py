from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.text import slugify
from datetime import datetime, timedelta
from rest_framework.exceptions import ValidationError as RestValidationError
from .models import Reminder

class DateCleanMixin:

     def clean_date(self):
        if self.cleaned_data['date'] < timezone.now().date():
            raise ValidationError("Date cannot be in the past")
        return self.cleaned_data['date']

class SlugDateTimeCleanMixin:

    def clean(self):
        if self.cleaned_data.get('date', None):
            if self.cleaned_data['date'] == timezone.localdate():
                if self.cleaned_data['time'] <= timezone.localtime().time():
                    raise ValidationError(
                        "If you want to see the notifications, set an offset of atleast 60 seconds.")
            timed_on = datetime.combine(self.cleaned_data['date'], self.cleaned_data['time'])
            self.cleaned_data['timed_on'] = timed_on

        self.cleaned_data['slug'] = self.slug_more(slugify('-'.join(self.cleaned_data['title'].split(maxsplit=12)[:12])))
        return self.cleaned_data

    def slug_more(self, slug):
        if slug in ('create', 'delete', 'update', 'edit', 'api', 'profile'):
            slug += '-1'
        suffix = 1
        if self.user.reminders.filter(slug=slug).exists():
            while(True):
                test_slug = slug
                test_slug += '-' + str(suffix)
                if self.user.reminders.filter(slug=test_slug).exists():
                    suffix += 1
                else:
                    return test_slug
        return slug

class DateValidateMixin:

    def validate_timed_on(self, value):
        if value <= timezone.localtime() + timedelta(seconds=5):
            raise RestValidationError('Set a reminder with an offset of atleast 10 seconds in the future')
        return value

class SlugValidateMixin:
    def validate_slug(self, value):
        value = self.slug_more(slugify('-'.join(value.split(maxsplit=12)[:12])))
        return value

    def slug_more(self, slug):
        if slug in ('create', 'delete', 'update', 'edit',):
            slug += '-1'
        suffix = 1
        if Reminder.objects.filter(user_id=self.initial_data['user']).filter(slug=slug).exists():
            while(True):
                test_slug = slug
                test_slug += '-' + str(suffix)
                if Reminder.objects.filter(user_id=self.initial_data['user']).filter(slug=test_slug).exists():
                    suffix += 1
                else:
                    return test_slug
        return slug