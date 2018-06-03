from django.urls import re_path
from .. import views


urlpatterns = [
    re_path(r'edit/$', views.ProfileView.as_view(), name='profile_edit'),
    re_path(r'^api/list/$', views.ProfileListRest.as_view()),
    re_path(r'^api/list/(?P<pk>\d+/$)', views.ProfileDetailRest.as_view()),
]
