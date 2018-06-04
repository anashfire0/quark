from django.shortcuts import render, Http404
from django.views import generic
from django.contrib.auth.views import (
    LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView,
    PasswordResetDoneView, PasswordResetCompleteView,
    )
from django.conf import settings
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, ProfileForm
from .models import Profile, CustomUser
from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from rest_framework import generics
from .serializers import ProfileSerializer, CustomUserSerializer

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

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('users:password_reset_complete')
    template_name = 'users/registration/password_reset_confirm.html'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/registration/password_reset_complete.html'


class ProfileView(LoginRequiredMixin, SuccessMessageMixin, generic.FormView):
    form_class = ProfileForm
    template_name = 'users/profile/profile_create.html'
    success_url = reverse_lazy('users:profile_edit')
    success_message = "Profile updated."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': get_user(self.request)})
        return kwargs

    def get(self, request, *args, **kwargs):
        self.user = get_user(request)
        try:
            self.initial={'email': self.user.email,
                        'first_name': self.user.first_name,
                        'last_name': self.user.last_name,
                        'phone_no':self.user.profile.phone_no,
                        'profile_pic': self.user.profile.profile_pic,
                        }
        except Profile.DoesNotExist:
            Profile(user=self.user).save()
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ProfileListRest(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileDetailRest(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class CustomUserListRest(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer