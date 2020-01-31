# django
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from apps.models import models as antropoloops_models
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
# app
from . import forms

class DashboardView(LoginRequiredMixin, ListView):
    """ User dashboard view """

    model = antropoloops_models.Audioset
    login_url = 'login'

    def get_queryset(self):
        current_user = self.request.user
        queryset = antropoloops_models.Audioset.objects.filter(
            owner=current_user
        ).order_by(
            'update_date'
        )
        return queryset

class AudiosetCreateView(CreateView):
    """ Audioset creation form in user dashboard """

    model = antropoloops_models.Audioset
    form_class  = forms.AudiosetCreateForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(AudiosetCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _(
            'Has creado el audioset con éxito. Ahora puedes añadirle '
            'tracks y clips'
        ))
        return reverse_lazy('audioset_update', kwargs={'slug' : self.object.slug })


class AudiosetDetailView(DetailView):
    """ Audioset detail view/ajax update form """

    model = antropoloops_models.Audioset
