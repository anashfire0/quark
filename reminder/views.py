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
    paginate_by = 8

    def get(self, request, *args, **kwargs):

        #implementing sorting
        if request.COOKIES.get('sorting_by'):
            sort_by=request.COOKIES.get('sorting_by')

        if request.GET.get('sort_by'):
            sort_by = request.GET.get('sort_by', 'timed_on').lower()

        if sort_by == 'recently-timed': 
            self.queryset = [x 
                            for x in 
                            Reminder.objects.recently_timed() 
                            if x.user_id == get_user(request).id
            ]
        elif sort_by == 'recently-created':
            self.queryset = [x 
                            for x in 
                            Reminder.objects.recently_created() 
                            if x.user_id == get_user(request).id
            ]
        else:
            self.queryset = get_user(request).reminders.order_by(sort_by)

        #implementing searching
        if request.GET.get('reminder_search', None):
            self.paginate_by = None
            self.queryset = get_user(request).reminders.filter(title__icontains=request.GET.get('reminder_search'))
            if not self.queryset.exists():
                messages.error(request, 'Not Found')
                # self.object_list = None #to use get_context_data
                # self.get_context_data(search_empty=
                #     'Did not find any title containing' 
                #     f'{request.GET.get("reminder_search")}.')
        response = super().get(request, *args, **kwargs)
        response.set_cookie('sorting_by', sort_by)
        return response


class ReminderDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'reminder/reminder_detail.html'
    context_object_name = 'reminder'

    def get(self, request, slug, *args, **kwargs):
        self.queryset = get_user(request).reminders.all()
        return super().get(request, slug, *args, **kwargs)

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
        obj = user.reminders.get(slug=slug)
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
        messages.success(request, 'Reminder successfully edited.')
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
        obj = get_user(request).reminders.get(slug__iexact=slug)
        return render(request, self.template_name, self.get_context_data(reminder=obj, **kwargs))

    def post(self, request, slug, *args, **kwargs):
        if request.POST['to_delete']:
            get_user(request).reminders.get(slug__iexact=slug).delete()
            messages.success(request, 'Reminder successfully deleted.')
            return redirect(self.success_url)
        return redirect(reverse_lazy('reminder:reminder_detail', args=[slug]))


class ReminderViewSet(viewsets.ModelViewSet):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)