from django.shortcuts import render
from django.views import generic
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.http import HttpResponse

# Create your views here.


class HomeView(generic.TemplateView):
    template_name = 'users/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'red': 'alskjdlajd'})
        return context

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context = super(CustomLoginView, self).get_context_data(**kwargs)
        context.update({'next': self.request.GET.get('next')}),
        return context

