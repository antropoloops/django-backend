# django
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
# app
from . import views

app_name = 'api'

urlpatterns = [
    # Tracks
    path(
        'track/crea',
        views.track_create,
        name='track_create'
    ),
    path(
        'track/edita',
        views.track_update,
        name='track_update'
    ),
    path(
        'track/ordena',
        views.track_sort,
        name='track_sort'
    ),
    path(
        'track/borra',
        views.track_delete,
        name='track_delete'
    ),
    path(
        'track/clips/<int:pk>',
        views.track_clips,
        name='track_clips'
    ),
    path(
        'track/<int:pk>',
        views.track,
        name='track'
    ),
    # Clips
    path(
        'clip/crea',
        views.clip_create,
        name='clip_create'
    ),
    path(
        'clip/edita',
        views.clip_update,
        name='clip_update'
    ),
    path(
        'clip/ordena',
        views.clip_sort,
        name='clip_sort'
    ),
    path(
        'clip/borra',
        views.clip_delete,
        name='clip_delete'
    ),
    path(
        'clip/<int:pk>',
        views.clip,
        name='clip'
    ),

    # Audioset
    path(
        'audioset/<slug:slug>',
        views.audioset,
        name='audioset'
    ),
    path(
        'audioset/toggle/<int:pk>',
        views.audioset_toggle,
        name='audioset_toggle'
    ),

    # Project
    path(
        'project/<slug:slug>',
        views.project,
        name='project'
    ),
    # Themes
    path(
        'theme/<slug:slug>',
        views.theme,
        name='theme'
    ),
    path(
        'theme/',
        views.themes,
        name='themes'
    ),

    # Custom paths
    # Project
    path(
        'index/<slug:slug>',
        views.resource,
        name='resource'
    ),
    # Home
    path(
        'index',
        views.projects,
        name='home'
    ),

    # Cache
    path(
        'clean/<slug:slug>',
        views.clean_cache,
        name='clean_cache'
    ),

]
