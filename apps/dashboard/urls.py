# django
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
# app
from . import views

urlpatterns = [
    path(
        'dashboard',
        views.DashboardView.as_view(),
        name='dashboard'
    ),
    path(
        'audioset/crea',
        views.AudiosetCreateView.as_view(),
        name='audioset_create'
    ),
    path(
        'audioset/<slug:slug>/configura',
        views.AudiosetUpdateView.as_view(),
        name='audioset_update'
    ),
    path(
        'audioset/<slug:slug>/gestiona-clips',
        views.AudiosetDetailView.as_view(),
        name='audioset_tracklist'
    ),
]
