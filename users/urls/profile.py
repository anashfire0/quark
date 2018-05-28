from django.urls import re_path
from .. import views


urlpatterns = [
    # re_path(r'^$', views.ProfileDetailView.as_view(), name='profile_display'),
    re_path(r'create/$', views.ProfileCreateView.as_view(), name='profile_create'),
    re_path(r'edit/$', views.ProfileEditView.as_view(), name='profile_edit'),
    # re_path(r'edit/$', views.ProfileEditView.as_view(), name='profile_edit'),
]
