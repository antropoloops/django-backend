# django
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
# app
from . import views

urlpatterns = [
    path(
        '',
        views.login_redirect,
        name='login_redirect'
    ),
    path(
        'mis-audiosets',
        views.AudiosetListView.as_view(),
        name='audioset_list'
    ),
    path(
        'proyectos',
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
        views.ProjectUpdateView.as_view(),
        name='project_update'
    ),
    path(
        'proyecto/<int:pk>/borra',
        views.ProjectDeleteView.as_view(),
        name='project_delete'
    ),
    path(
        'proyecto/<int:pk>',
        views.ProjectDetailView.as_view(),
        name='project_detail'
    ),
    path(
        'proyecto/<int:pk>/crea-audioset',
        views.AudiosetCreateView.as_view(),
        name='audioset_create'
    ),
    path(
        'audioset/crea',
        views.AudiosetCreateView.as_view(),
        name='audioset_create_alt'
    ),
    path(
        'audioset/<int:pk>/borra',
        views.AudiosetDeleteView.as_view(),
        name='audioset_delete'
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
