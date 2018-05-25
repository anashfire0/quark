from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.base import ContextMixin
from .models import Reminder
from .forms import CreateReminderForm

# Create your views here.

class ReminderListView(generic.ListView):
    model = Reminder
    template_name = 'reminder/reminder_list.html'
    context_object_name = 'reminders'

class ReminderDetailView(generic.DetailView):
    model = Reminder
    template_name = 'reminder/reminder_detail.html'
    context_object_name = 'reminder'

class CreateReminderView(ContextMixin, generic.View):
    template_name = 'reminder/create_reminder.html'
    form_class = CreateReminderForm
    success_url = reverse_lazy('reminder:reminder_list')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data(
            form = self.form_class(), **kwargs))

    def post(self, request, *args, **kwargs):
        print(str(request.POST).center(1000, '$'))
        bound_form = self.form_class(request.POST)
        context = self.get_context_data(**kwargs)
        context.update({'form': bound_form})
        if not bound_form.is_valid():
            return render(request, self.template_name, context)
        if bound_form.is_valid():
            return redirect(bound_form.save()) 

