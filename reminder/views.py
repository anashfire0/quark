from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.base import ContextMixin
from .models import Reminder
from .forms import CreateReminderForm, EditReminderForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class ReminderListView(LoginRequiredMixin, generic.ListView):
    model = Reminder
    template_name = 'reminder/reminder_list.html'
    context_object_name = 'reminders'

class ReminderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Reminder
    template_name = 'reminder/reminder_detail.html'
    context_object_name = 'reminder'

class CreateReminderView(LoginRequiredMixin, ContextMixin, generic.View):
    template_name = 'reminder/create_reminder.html'
    form_class = CreateReminderForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data(
            form = self.form_class(), **kwargs))

    def post(self, request, *args, **kwargs):
        bound_form = self.form_class(request.POST)
        if not bound_form.is_valid():
            context = self.get_context_data(**kwargs)
            context.update({'form': bound_form})
            return render(request, self.template_name, context)
        return redirect(bound_form.save()) 

class  EditReminderView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'reminder/reminder_update.html'
    form_class = EditReminderForm
    model = Reminder

    def get(self, request, slug, *args, **kwargs):
        obj = self.model.objects.get(slug=slug)
        initial = {'user' : obj.user,
        'title' : obj.title,
        'text' : obj.text,
        'date' : obj.timed_on.date(),
        'time' : obj.timed_on.time().replace(second=0),}
        stored_form = self.form_class(initial=initial)
        return render(request, self.template_name, self.get_context_data(
            form=stored_form, **kwargs))

    def post(self, request, slug, *args, **kwargs):
        bound_form = self.form_class(request.POST)
        if not bound_form.is_valid():
            context = self.get_context_data(**kwargs)
            context.update({'form': bound_form})
            return render(request, self.template_name, context)
        return redirect(bound_form.save(slug))

class DeleteReminderView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'reminder/reminder_delete.html'
    model = Reminder
    success_url = reverse_lazy('reminder:reminder_list')

    def get(self, request, slug, *args, **kwargs):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        return render(request, self.template_name, self.get_context_data(reminder= obj, **kwargs))

    def post(self, request, slug, *args, **kwargs):
        if request.POST['to_delete']:
            self.model.objects.get(slug__iexact=slug).delete()
            return redirect(self.success_url)
        return redirect(reverse_lazy('reminder:reminder_detail', args=[slug]))