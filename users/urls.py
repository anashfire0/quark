from django.urls import re_path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    re_path('^login/$', views.CustomLoginView.as_view(), name='login'),
    re_path('^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    re_path('^signup/$', views.SignUpView.as_view(), name='signup'),
    re_path('^password/change/$',
            views.CustomPasswordChangeView.as_view(), name='password_change'),
    re_path('^password/change/complete/$',
            auth_views.PasswordChangeDoneView.as_view(template_name='users/registration/password_change_complete.html'), name='password_change_complete'),
]
