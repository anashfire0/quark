from django.urls import re_path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    re_path('^login/$', views.CustomLoginView.as_view(), name='login'),
    re_path('^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    re_path('^signup/$', views.SignUpView.as_view(), name='signup'),
]
