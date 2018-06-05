"""quark URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import RedirectView
from users.views import HomeView
from reminder.views import ReminderViewSet
from users.views import UserViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', HomeView.as_view(), name='home'),
    re_path(r'^users/', include('users.urls.users',)),
    re_path(r'^reminders/', include('reminder.urls')),
    re_path(r'^api-auth/', include('rest_framework.urls')),
]

#api urls
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'reminders', ReminderViewSet)
router.register(r'users', UserViewSet)

urlpatterns += [
    re_path(r'^apis/', include(router.urls))
]