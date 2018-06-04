from django.urls import re_path
from . import views 

from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'reminder'

urlpatterns = [
    re_path(r'^$', views.ReminderListView.as_view(), name='reminder_list'),
    re_path(r'^create/$', views.CreateReminderView.as_view(), name='create_reminder'),
    re_path(r'^api/list/$', views.ReminderListRest.as_view()),
    re_path(r'^api/list/(?P<pk>\d+)/$', views.ReminderDetailRest.as_view()),
    re_path(r'^(?P<slug>[\w\-]+)/edit/$', views.EditReminderView.as_view(), name='edit_reminder'),
    re_path(r'^(?P<slug>[\w\-]+)/delete/$', views.DeleteReminderView.as_view(), name='delete_reminder'),
    re_path(r'^(?P<slug>[\w\-]+)/$', views.ReminderDetailView.as_view(), name='reminder_detail'),

    ]

urlpatterns = format_suffix_patterns(urlpatterns)