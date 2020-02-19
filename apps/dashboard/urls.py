# django
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
# app
from . import views

urlpatterns = [
    path(
        'dashboard',
        views.ProjectListView.as_view(),
        name='project_list'
    ),
    path(
        'proyecto/crea',
        views.ProjectCreateView.as_view(),
        name='project_create'
    ),
    path(
        'proyecto/<int:pk>/edita',
        views.ProjectDetailView.as_view(),
        name='project_detail'
    ),
    path(
        'proyecto/<int:pk>/crea-audioset',
        views.AudiosetCreateView.as_view(),
        name='audioset_create'
    ),
    path(
        'audioset/<int:pk>/configura',
        views.AudiosetUpdateView.as_view(),
        name='audioset_update'
    ),
    path(
        'audioset/<int:pk>/gestiona-clips',
        views.AudiosetTracklistView.as_view(),
        name='audioset_tracklist'
    ),
]
