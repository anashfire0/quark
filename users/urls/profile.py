from django.urls import re_path
from .. import views


urlpatterns = [
    re_path(r'edit/$', views.ProfileView.as_view(), name='profile_edit'),
]
