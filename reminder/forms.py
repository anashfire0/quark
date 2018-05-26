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
    user = forms.ModelChoiceField(get_user_model().objects.all())
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
            'user': self.cleaned_data['user'],
            'title': self.cleaned_data['title'],
            'text': self.cleaned_data['text'],
            'slug': self.cleaned_data['slug'],
            'timed_on': self.cleaned_data['timed_on'],
            'reminded_count': 0,
        }
        obj = Reminder(**reminder_entry)
        if commit:
            obj.save()
            return reverse_lazy('reminder:reminder_list')
        else:
            return obj


class EditReminderForm(
    DateCleanMixin, SlugDateTimeCleanMixin,
        BaseReminderForm):

    def clean_title(self):
        return self.cleaned_data['title'].lower()

    def save(self, slug, commit=True):
        obj = Reminder.objects.get(slug__iexact=slug)
        obj.user = self.cleaned_data['user']
        obj.title =self.cleaned_data['title']
        obj.text =self.cleaned_data['text']
        obj.timed_on = self.cleaned_data['timed_on']
        if commit:
            obj.save()
            return reverse_lazy('reminder:reminder_list')
        else:
            return obj
