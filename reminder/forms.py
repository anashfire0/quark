from django import forms
from django.contrib.auth import get_user_model
from datetime import datetime
from .models import Reminder
from django.urls import reverse_lazy
from .utils import DateCleanMixin, SlugDateTimeCleanMixin


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class BaseReminderForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    title = forms.CharField(max_length=256)
    text = forms.CharField(widget=forms.Textarea())
    date = forms.DateField(widget=DateInput())
    time = forms.TimeField(widget=TimeInput())


class CreateReminderForm(
        DateCleanMixin, SlugDateTimeCleanMixin,
        BaseReminderForm):

    def clean_title(self):
        return self.cleaned_data['title'].lower()

    def save(self, commit=True):
        reminder_entry = {
            'user': self.user,
            'title': self.cleaned_data['title'],
            'text': self.cleaned_data['text'],
            'slug': self.cleaned_data['slug'],
            'timed_on': self.cleaned_data['timed_on'],
            'reminded_count': 0,
        }
        obj = Reminder(**reminder_entry)
        if commit:
            obj.save()
            return obj
        else:
            return obj


class EditReminderForm(
    DateCleanMixin, SlugDateTimeCleanMixin,
        BaseReminderForm):

    def clean_title(self):
        return self.cleaned_data['title'].lower()

    def save(self, slug, commit=True):
        obj = self.user.reminders.get(slug__iexact=slug)
        obj.user = self.user
        obj.title =self.cleaned_data['title']
        obj.slug = self.cleaned_data['slug']
        obj.text =self.cleaned_data['text']
        obj.timed_on = self.cleaned_data['timed_on']
        if commit:
            obj.save()
            return obj
        else:
            return obj
