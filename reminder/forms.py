from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError, MultipleObjectsReturned
from django.utils import timezone
from django.utils.text import slugify
from datetime import datetime 
from .models import Reminder


class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class CreateReminderForm(forms.Form):
    user = forms.ModelChoiceField(get_user_model().objects.all())
    title = forms.CharField(max_length=256)
    text = forms.CharField(widget=forms.Textarea())
    date = forms.DateField(widget=DateInput())
    time = forms.TimeField(widget=TimeInput())

    def clean_title(self):
        return self.cleaned_data['title'].lower()

    def clean_date(self):
        if self.cleaned_data['date'] < timezone.now().date(): 
            raise ValidationError("Date cannot be in the past")
        return self.cleaned_data['date']

    def clean(self):
        if self.cleaned_data['date'] == timezone.now().date():
            if self.cleaned_data['time'] <= timezone.now().time():
                raise ValidationError("If you want to see the notifications, set an offset of atleast 60 seconds.")
        timed_on = datetime.combine(self.cleaned_data['date'], self.cleaned_data['time'])
        self.cleaned_data['timed_on'] = timed_on
        return self.cleaned_data

    def save(self, commit=True):
        slug = slugify(''.join(self.cleaned_data['title'].split(maxsplit=12)[:12]))
        slug = self.slug_more(slug)
        reminder_entry = {
        'user' : self.cleaned_data['user'],
        'title': self.cleaned_data['title'],
        'text' : self.cleaned_data['text'],
        'slug' : slug,
        'timed_on': self.cleaned_data['timed_on'],
        'reminded_count': 0,
        }
        obj = Reminder(reminder_entry)

    def slug_more(self, slug):
        User = get_user_model()
        obj = User.objects.get(username=self.cleaned_data['user'])
        suffix = 1
        while(True):
            test_slug = slug
            test_slug += str(suffix)
            if obj.reminders.filter(slug=test_slug).exists():
                suffix += 1
            else:
                return slug
