# django
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from apps.models import models as antropoloops_models
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import Http404
# app
from . import forms


def login_redirect(request):
    """
    Redirects users based on whether they are in the admins group
    """

    if request.user.is_staff:
        return redirect("project_list")
    else:
        return redirect("audioset_list")


class AudiosetListView(LoginRequiredMixin, ListView):
    """ User dashboard view """

    model = antropoloops_models.Audioset
    login_url = 'login'

    def get_queryset(self):
        current_user = self.request.user
        queryset = antropoloops_models.Audioset.objects.all().order_by(
            '-update_date'
        )
        if not current_user.is_staff:
            queryset = queryset.filter(owner=current_user)
        return queryset

class ProjectListView(LoginRequiredMixin, ListView):
    """ User dashboard view """

    model = antropoloops_models.Project
    login_url = 'login'

    def get_queryset(self):
        current_user = self.request.user
        queryset = antropoloops_models.Project.objects.all().order_by(
            '-update_date'
        )
        if not current_user.is_staff:
            queryset = queryset.filter(owner=current_user)
        return queryset


class ProjectDetailView(LoginRequiredMixin, DetailView):
    """ User dashboard view """

    model = antropoloops_models.Project
    login_url = 'login'

    def get_object(self, *args, **kwargs):
        obj = super(ProjectDetailView, self).get_object(*args, **kwargs)
        if not obj.is_owned_by(self.request.user):
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        """Pass context data to generic view."""

        audioset_list = antropoloops_models.Audioset.objects.filter(
            project=self.object
        )
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['audioset_list'] = audioset_list
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    """ Project creation form in user dashboard. """

    model = antropoloops_models.Project
    form_class  = forms.ProjectForm

    def get_context_data(self, **kwargs):
        """Pass context data to generic view."""

        context = super(ProjectCreateView, self).get_context_data(**kwargs)
        context['page_title'] = _('Crea un proyecto nuevo')
        context['submit_text'] = _('Crear proyecto')
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(ProjectCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _(
            'Has creado el proyecto con éxito'
        ))
        return reverse_lazy('project_detail', kwargs={'pk' : self.object.pk })


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    """ Project update form in user dashboard. """

    model = antropoloops_models.Project
    form_class  = forms.ProjectForm

    def get_object(self, *args, **kwargs):
        obj = super(ProjectUpdateView, self).get_object(*args, **kwargs)
        if not obj.is_owned_by(self.request.user):
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        """Pass context data to generic view."""

        context = super(ProjectUpdateView, self).get_context_data(**kwargs)
        context['page_title']  = _('Editar «{}» ' . format(context['object'].name));
        context['submit_text'] = _('Guardar cambios')
        return context

    def get_success_url(self):
        messages.success(self.request, _(
            'Has editado el proyecto con éxito'
        ))
        return reverse_lazy('project_detail', kwargs={'pk' : self.object.pk })


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    """ Project delete form in user dashboard """

    model = antropoloops_models.Project
    success_url = reverse_lazy('project_list')

    def get_object(self, *args, **kwargs):
        obj = super(ProjectDeleteView, self).get_object(*args, **kwargs)
        if not obj.is_owned_by(self.request.user):
            raise Http404
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(
            self.request,
            _('El proyecto ha sido borrado con éxito')
        )
        return super(ProjectDeleteView, self).delete(request, *args, **kwargs)


class AudiosetCreateView(LoginRequiredMixin, CreateView):
    """ Audioset creation form in user dashboard. """

    model         = antropoloops_models.Audioset
    form_class    = forms.AudiosetForm
    template_name = 'models/audioset_form.html'

    def dispatch(self, *args, **kwargs):
        if 'pk' in kwargs:
            self.project = get_object_or_404(
                antropoloops_models.Project,
                pk=kwargs.get('pk')
            )
        else:
            self.project, created = antropoloops_models.Project.objects.get_or_create(
                antropoloops_models.Project,
                slug='comunidad'
            )
        return super(AudiosetCreateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        """Pass context data to generic view."""
        context = super(AudiosetCreateView, self).get_context_data(**kwargs)
        if hasattr(self, 'project'):
            context['project'] = self.project
        return context

    def form_valid(self, form):
        form.instance.owner   = self.request.user
        form.instance.project = self.project
        return super(AudiosetCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _(
            'Has añadido éxitosamente el audioset'
        ))
        if self.request.user.is_staff:
            return reverse_lazy(
                'project_detail',
                kwargs={ 'pk' : self.project.pk }
            )
        return reverse_lazy('audioset_list')


class AudiosetUpdateView(LoginRequiredMixin, UpdateView):
    """ Audioset update form in user dashboard """

    model = antropoloops_models.Audioset
    form_class  = forms.AudiosetForm
    template_name = 'models/audioset_form.html'

    def get_object(self, *args, **kwargs):
        obj = super(AudiosetUpdateView, self).get_object(*args, **kwargs)
        if not obj.is_owned_by(self.request.user):
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        """Pass context data to generic view."""
        context = super(AudiosetUpdateView, self).get_context_data(**kwargs)
        context['project']  = self.object.project
        context['audioset_name'] = self.object.name
        context['audioset_slug'] = self.object.slug
        return context

    def get_success_url(self):
        messages.success(self.request, _(
            'Has configurado el audioset con éxito. Ahora puedes añadirle '
            'tracks y clips'
        ))
        return reverse_lazy('audioset_tracklist', kwargs={'pk' : self.object.pk })


class AudiosetDeleteView(LoginRequiredMixin, DeleteView):
    """ Audioset delete form in user dashboard """

    model = antropoloops_models.Audioset

    def get_object(self, *args, **kwargs):
        obj = super(AudiosetDeleteView, self).get_object(*args, **kwargs)
        if not obj.is_owned_by(self.request.user):
            raise Http404
        return obj

    def get_success_url(self):
        return reverse_lazy(
            'audioset_list',
        )

    def delete(self, request, *args, **kwargs):
        messages.success(
            self.request,
            _('El audioset ha sido borrado con éxito')
        )
        return super(AudiosetDeleteView, self).delete(self, request, *args, **kwargs)


class AudiosetTracklistView(LoginRequiredMixin, DetailView):
    """ Audioset detail view/ajax update form """

    model = antropoloops_models.Audioset
    template_name = 'models/audioset_tracklist_form.html'

    def get_object(self, *args, **kwargs):
        obj = super(AudiosetTracklistView, self).get_object(*args, **kwargs)
        if not obj.is_owned_by(self.request.user):
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super(AudiosetTracklistView, self).get_context_data(**kwargs)
        context['tracks'] = antropoloops_models.Track.objects.filter(
            audioset = self.object
        )
        context['clipsnumber'] = antropoloops_models.Clip.objects.filter(
            track__in = context['tracks']
        ).count()
        context['trackform'] = forms.TrackUpdateFormAjax(initial={'audioset' : self.kwargs['pk']})
        context['clipform']  = forms.ClipUpdateForm(initial={'audioset' : self.kwargs['pk']})
        return context
