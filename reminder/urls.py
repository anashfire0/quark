from django.urls import re_path
from . import views 

app_name = 'reminder'

urlpatterns = [
    re_path('^$', views.ReminderListView.as_view(), name='reminder_list'),
    re_path('^create/$', views.CreateReminderView.as_view(),{'what':'what'}, name='create_reminder'),
    re_path('^(?P<slug>[\w\-]+)/$', views.ReminderDetailView.as_view(), name='reminder_detail'),
    ]