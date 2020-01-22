# django
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path(
        'login',
        auth_views.LoginView.as_view(),
        name='login'
    ),
    path(
        'logout',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
    path(
        'chao',
        auth_views.TemplateView.as_view(template_name='registration/chao.html'),
        name='goodbye'
    ),
    path(
        'cambia-tu-password',
        auth_views.PasswordResetView.as_view(),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        views.password_reset_done,
        name='password_reset_done'
    ),
    re_path(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'reset/done',
        views.password_reset_complete,
        name='password_reset_complete'
    ),
]
