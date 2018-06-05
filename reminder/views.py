from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.base import ContextMixin
from .models import Reminder
from .forms import CreateReminderForm, EditReminderForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user
from django.contrib import messages
from django.core.mail import send_mail

from .tasks import raka, email_reminder

from .permissions import IsOwnerOrReadOnly
from .serializers import ReminderSerializer

from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets

# Create your views here.


class ReminderListView(LoginRequiredMixin, generic.ListView):
    template_name = 'reminder/reminder_list.html'
    context_object_name = 'reminders'

    def get(self, request, *args, **kwargs):
        raka.apply_async(('Kan hai re raka',), countdown=2)
        self.queryset = get_user(request).reminders.all()
        return super().get(request, *args, **kwargs)


class ReminderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Reminder
    template_name = 'reminder/reminder_detail.html'
    context_object_name = 'reminder'


class CreateReminderView(LoginRequiredMixin, ContextMixin, generic.View):
    template_name = 'reminder/create_reminder.html'
    form_class = CreateReminderForm

    def get(self, request, *args, **kwargs):
        user = get_user(request)
        return render(request, self.template_name, self.get_context_data(
            form=self.form_class(user=user), **kwargs))

    def post(self, request, *args, **kwargs):
        user = get_user(request)
        bound_form = self.form_class(request.POST, user=user)

        if not bound_form.is_valid():
            context = self.get_context_data(**kwargs)
            context.update({'form': bound_form})
            messages.warning(request, 'Please correct the errors')
            return render(request, self.template_name, context)
        reminder = bound_form.save()
        self.set_email_reminder(reminder)
        messages.success(request, 'Reminder successfully set.')
        return redirect(reverse_lazy('reminder:edit_reminder', args=[reminder.slug, ]))

    def set_email_reminder(self, reminder):
        subject = reminder.title
        body = reminder.text
        sender = 'Reminder@quark.com'
        receiver = reminder.user.email
        slug = reminder.slug
        email_reminder.apply_async(
            (subject, body, sender, receiver, slug), eta=reminder.timed_on.astimezone())


class EditReminderView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'reminder/reminder_update.html'
    form_class = EditReminderForm
    model = Reminder

    def get(self, request, slug, *args, **kwargs):
        user = get_user(request)
        obj = self.model.objects.get(slug=slug)
        initial = {'user': obj.user,
                   'title': obj.title,
                   'text': obj.text,
                   'date': obj.timed_on.astimezone().date(),
                   'time': obj.timed_on.astimezone().time().replace(second=0),
                   }
        stored_form = self.form_class(initial=initial, user=user)
        return render(request, self.template_name, self.get_context_data(
            form=stored_form, **kwargs))

    def post(self, request, slug, *args, **kwargs):
        user = get_user(request)
        bound_form = self.form_class(request.POST, user=user)

        if not bound_form.is_valid():
            context = self.get_context_data(**kwargs)
            context.update({'form': bound_form})
            messages.warning(request, 'Please correct the errors')
            return render(request, self.template_name, context)

        reminder = bound_form.save(slug, commit=True)
        self.set_email_reminder(reminder)
        messages.success(request, 'Reminder successfully set.')
        return redirect(reverse_lazy('reminder:edit_reminder', args=[reminder.slug]))

    def set_email_reminder(self, reminder):
        subject = reminder.title
        body = reminder.text
        sender = 'Reminder@quark.com'
        receiver = reminder.user.email
        slug = reminder.slug
        email_reminder.apply_async(
            (subject, body, sender, receiver, slug), eta=reminder.timed_on.astimezone())


class DeleteReminderView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'reminder/reminder_delete.html'
    model = Reminder
    success_url = reverse_lazy('reminder:reminder_list')

    def get(self, request, slug, *args, **kwargs):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        return render(request, self.template_name, self.get_context_data(reminder=obj, **kwargs))

    def post(self, request, slug, *args, **kwargs):
        if request.POST['to_delete']:
            self.model.objects.get(slug__iexact=slug).delete()
            messages.success(request, 'Reminder successfully deleted.')
            return redirect(self.success_url)
        return redirect(reverse_lazy('reminder:reminder_detail', args=[slug]))


class ReminderViewSet(viewsets.ModelViewSet):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)