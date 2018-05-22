from django.urls import re_path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    re_path('^login/$', views.CustomLoginView.as_view(), name='login'),
    re_path('^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    re_path('^signup/$', views.SignUpView.as_view(), name='signup'),
    re_path('^password_change/$',
            views.CustomPasswordChangeView.as_view(), name='password_change'),
    re_path('^password_change/complete/$',
            auth_views.PasswordChangeDoneView.as_view(template_name='users/registration/password_change_complete.html'), name='password_change_complete'),
    re_path('^password_reset/$', views.CustomPasswordResetView.as_view(),
            name='password_reset'),
    re_path('^password_reset/done/$',
            views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path('^password_reset_confirm/(?P<uidb64>\w+)/(?P<token>[\w\-]+)/$',
            views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    re_path('^password_reset_confirm/complete/$',
            views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
