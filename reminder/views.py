from django.shortcuts import render
from django.views import generic
from .models import Reminder

# Create your views here.

class ReminderListView(generic.ListView):
    model = Reminder
    template_name = 'reminder/reminder_list.html'
    context_object_name = 'reminders'

class ReminderDetailView(generic.DetailView):
    model = Reminder
    template_name = 'reminder/reminder_detail.html'
    context_object_name = 'reminder'