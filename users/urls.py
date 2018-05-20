from django.urls import re_path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    re_path('^login/$', views.CustomLoginView.as_view(), name='login'),
    re_path('^logout/$', LogoutView.as_view(), name='logout'),
]
