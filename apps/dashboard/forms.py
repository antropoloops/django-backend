# django
from django import forms
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _
from django.forms.models import inlineformset_factory
# app
from apps.models import models as antropoloops_models
from apps.limited_textarea_widget.widgets import LimitedTextareaWidget
from apps.image_preview_widget.widgets import ImagePreviewWidget

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


class ProjectCreateForm(forms.ModelForm):

    class Meta:
        model = antropoloops_models.Project
        fields = [
            'name',
            'description',
        ]
        widgets = {
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

class ClipForm(forms.ModelForm):
    class Meta:
        model = antropoloops_models.Clip
        exclude = ('audio', )

class InlineAudioForm(forms.ModelForm):
    class Meta:
        model = antropoloops_models.Audio
        fields = '__all__'
