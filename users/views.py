from django.shortcuts import render
from django.views import generic
from django.contrib.auth.views import (
    LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView,
    PasswordResetDoneView, PasswordResetCompleteView,
    )
from django.conf import settings
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm

# Create your views here.


class HomeView(generic.TemplateView):
    template_name = 'users/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'red': 'alskjdlajd'})
        return context


class CustomLoginView(LoginView):
    template_name = 'users/registration/login.html'

    def get_context_data(self, **kwargs):
        context = super(CustomLoginView, self).get_context_data(**kwargs)
        next = self.request.GET.get(
            'next', '') if not reverse_lazy('users:signup') else ''
        context.update({'next': next}),
        return context


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/registration/signup.html'
    success_url = reverse_lazy('users:login')

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'users/registration/password_change.html'
    success_url = reverse_lazy('users:password_change_complete')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/registration/password_reset_form.html'
    email_template_name = 'users/registration/password_reset_email.html'
    subject_template_name = 'users/registration/password_reset_subject.txt'
    success_url = reverse_lazy('users:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/registration/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('users:password_reset_complete')
    template_name = 'users/registration/password_reset_confirm.html'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/registration/password_reset_complete.html'