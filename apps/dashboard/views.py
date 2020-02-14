# django
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from apps.models import models as antropoloops_models
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
# app
from . import forms


class ProjectListView(LoginRequiredMixin, ListView):
    """ User dashboard view """

    model = antropoloops_models.Project
    login_url = 'login'

    def get_queryset(self):
        current_user = self.request.user
        queryset = antropoloops_models.Project.objects.filter(
            owner=current_user
        ).order_by(
            '-update_date'
        )
        return queryset


class ProjectDetailView(LoginRequiredMixin, DetailView):
    """ User dashboard view """

    model = antropoloops_models.Project
    login_url = 'login'

    def get_context_data(self, **kwargs):
        """Pass context data to generic view."""

        audioset_list = antropoloops_models.Audioset.objects.filter(
            project=self.object
        )
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['audioset_list'] = audioset_list
        return context


class ProjectCreateView(CreateView):
    """ Project creation form in user dashboard. """

    model = antropoloops_models.Project
    form_class  = forms.ProjectCreateForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(ProjectCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _(
            'Has creado el proyecto con éxito'
        ))
        return reverse_lazy('project_detail', kwargs={'slug' : self.object.slug })


class AudiosetCreateView(CreateView):
    """ Audioset creation form in user dashboard. """

    model = antropoloops_models.Audioset
    form_class  = forms.AudiosetCreateForm

    def form_valid(self, form):
        project = antropoloops_models.Project.objects.get(
            pk=self.kwargs.get('pk')
        )
        form.instance.owner  = self.request.user
        form.instance.project = project
        return super(AudiosetCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _(
            'Has añadido éxitosamente el audioset'
        ))
        return reverse_lazy('project_detail', kwargs={
            'pk' : self.kwargs.get('pk')
        })


class AudiosetUpdateView(UpdateView):
    """ Audioset update form in user dashboard """

    model = antropoloops_models.Audioset
    form_class  = forms.AudiosetUpdateForm
    template_name = 'models/audioset_configuration_form.html'

    def get_context_data(self, **kwargs):
        """Pass context data to generic view."""
        context = super(AudiosetUpdateView, self).get_context_data(**kwargs)
        context['audioset_name'] = self.object.name
        context['audioset_slug'] = self.object.slug
        return context

    def get_success_url(self):
        messages.success(self.request, _(
            'Has configurado el audioset con éxito. Ahora puedes añadirle '
            'tracks y clips'
        ))
        return reverse_lazy('audioset_tracklist', kwargs={'slug' : self.object.slug })


class AudiosetDetailView(DetailView):
    """ Audioset detail view/ajax update form """

    model = antropoloops_models.Audioset

    def get_context_data(self, request):
        tracks = antropoloops_models.Track.objects.filter(
            audioset = self.object.instance
        )

    def get_context_data(self, **kwargs):
        context = super(AudiosetDetailView, self).get_context_data(**kwargs)
        context['tracks'] = antropoloops_models.Track.objects.filter(
            audioset = self.object
        )
        context['trackform'] = forms.TrackForm
        context['clipform']  = forms.ClipForm
        context['audioform'] = forms.InlineAudioForm
        return context
