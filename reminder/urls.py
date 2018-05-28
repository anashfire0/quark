from django.urls import re_path
from . import views 

app_name = 'reminder'

urlpatterns = [
    re_path('^$', views.ReminderListView.as_view(), name='reminder_list'),
    re_path('^create/$', views.CreateReminderView.as_view(), name='create_reminder'),
    re_path('^(?P<slug>[\w\-]+)/edit/$', views.EditReminderView.as_view(), name='edit_reminder'),
    re_path('^(?P<slug>[\w\-]+)/delete/$', views.DeleteReminderView.as_view(), name='delete_reminder'),
    re_path('^(?P<slug>[\w\-]+)/$', views.ReminderDetailView.as_view(), name='reminder_detail'),
    ]