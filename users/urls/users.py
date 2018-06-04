from django.urls import re_path, include
from .. import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    re_path(r'^profile/', include('users.urls.profile')),
    re_path(r'^api/', views.CustomUserListRest.as_view()),
    re_path(r'^login/$', views.CustomLoginView.as_view(), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'^signup/$', views.SignUpView.as_view(), name='signup'),
    re_path(r'^password_change/$',
            views.CustomPasswordChangeView.as_view(), name='password_change'),
    re_path(r'^password_change/complete/$',
            auth_views.PasswordChangeDoneView.as_view(template_name='users/registration/password_change_complete.html'), name='password_change_complete'),
    re_path(r'^password_reset/$', views.CustomPasswordResetView.as_view(),
            name='password_reset'),
    re_path(r'^password_reset/done/$',
            views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(r'^password_reset_confirm/(?P<uidb64>\w+)/(?P<token>[\w\-]+)/$',
            views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    re_path(r'^password_reset_confirm/complete/$',
            views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
