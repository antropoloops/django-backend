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
        'track/clips',
        views.track_clips,
        name='track_clips'
    ),
    path(
        'track/',
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
        'clip/',
        views.clip,
        name='clip'
    ),

    path(
        'audioset/<int:pk>',
        views.audioset,
        name='audioset'
    ),
    # Audiosets
    path(
        'project/<int:pk>',
        views.project,
        name='project'
    ),
]
