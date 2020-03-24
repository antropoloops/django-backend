# django
from django import forms
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _
from django.forms.models import inlineformset_factory
# app
from apps.models import models as antropoloops_models
from apps.limited_textarea_widget.widgets import LimitedTextareaWidget
from apps.image_preview_widget.widgets import ImagePreviewWidget


def namedWidget(input_name, widget=forms.CharField):
    if isinstance(widget, type):
        widget = widget()
    render = widget.render
    widget.render = lambda name, value, attrs=None, renderer=None: render(input_name, value, attrs, renderer)
    return widget

class AudiosetCreateForm(forms.ModelForm):

    class Meta:
        model = antropoloops_models.Audioset
        fields = [
            'name',
            'description',
        ]
        widgets = {
            'description' : LimitedTextareaWidget(limit=280),
        }


class ProjectForm(forms.ModelForm):

    class Meta:
        model = antropoloops_models.Project
        fields = [
            'name',
            'image',
            'description',
        ]
        widgets = {
            'image' : ImagePreviewWidget(),
            'description' : LimitedTextareaWidget(limit=280),
        }

class AudiosetUpdateForm(forms.ModelForm):

    class Meta:
        model = antropoloops_models.Audioset
        fields = [
            'logo',
            'readme',
            'mode_display',
            'background'
        ]
        widgets = {
            'logo' : ImagePreviewWidget(
                placeholder=_(
                    "Añade aquí una imagen de cabecera"
                )
            ),
            'mode_display' : widgets.RadioSelect(),
            'background' : ImagePreviewWidget(
                placeholder=_(
                    "Añade aquí la imagen de fondo del panel"
                )
            ),
        }

class TrackForm(forms.ModelForm):
    class Meta:
        model = antropoloops_models.Track
        fields = [
            'name',
            'color',
        ]

class TrackFormAjax(forms.ModelForm):

    class Meta:
        model = antropoloops_models.Track
        fields = [
            'name',
            'color',
            'audioset'
        ]
        widgets = {
            'audioset' : widgets.HiddenInput()
        }


class TrackUpdateFormAjax(forms.ModelForm):

    pk = forms.IntegerField(
        widget=widgets.HiddenInput()
    )

    class Meta:
        model = antropoloops_models.Track
        fields = [
            'name',
            'color',
            'audioset'
        ]
        widgets = {
            'audioset' : widgets.HiddenInput()
        }


class ClipForm(forms.ModelForm):
    class Meta:
        model = antropoloops_models.Clip
        fields = '__all__'


class ClipFormAjax(forms.ModelForm):

    class Meta:
        model = antropoloops_models.Clip
        fields = '__all__'


class ClipUpdateFormAjax(forms.ModelForm):

    pk = forms.IntegerField(
        widget=widgets.HiddenInput()
    )

    class Meta:
        model = antropoloops_models.Clip
        fields = '__all__'
