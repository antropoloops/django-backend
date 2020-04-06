# python
from functools import reduce
# django
from django import forms
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _
from django.forms.models import inlineformset_factory
from django.core.exceptions import ValidationError
# app
from apps.models import models as antropoloops_models
from apps.limited_textarea_widget.widgets import LimitedTextareaWidget
from apps.image_preview_widget.widgets import ImagePreviewWidget
from apps.autoslug_widget.widgets import AutoslugWidget

def namedWidget(input_name, widget=forms.CharField):
    if isinstance(widget, type):
        widget = widget()
    render = widget.render
    widget.render = lambda name, value, attrs=None, renderer=None: render(input_name, value, attrs, renderer)
    return widget

class AudiosetCreateForm(forms.ModelForm):

    slug = forms.SlugField(
        label=_('Ruta'),
        help_text=_(
            'Esta campo contiene el fragmento final de la URL del proyecto'
        ),
        widget=AutoslugWidget(src='name')
    )

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if antropoloops_models.Audioset.objects.filter(slug=slug).exists():
            raise ValidationError(_(
                'Ya existe un audioset con esa ruta. Por favor, '
                'cámbiala ligeramente'
            ))
        return slug

    class Meta:
        model = antropoloops_models.Audioset
        fields = [
            'name',
            'slug',
            'description',
        ]
        widgets = {
            'description' : LimitedTextareaWidget(limit=280),
        }

class ProjectForm(forms.ModelForm):

    slug = forms.SlugField(
        label=_('Ruta'),
        help_text=_(
            'Este campo contiene el fragmento final de la URL del proyecto'
        ),
        widget=AutoslugWidget(src='name')
    )

    class Meta:
        model = antropoloops_models.Project
        fields = [
            'name',
            'slug',
            'image',
            'description',
            'readme',
            'background',
        ]
        widgets = {
            'image' : ImagePreviewWidget(),
            'background'  : ImagePreviewWidget(),
            'description' : LimitedTextareaWidget(limit=280),
        }

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if antropoloops_models.Project.objects.filter(slug=slug).exists():
            raise ValidationError(_(
                'Ya existe un proyecto con esa ruta. Por favor, '
                'cámbiala ligeramente. Por ejemplo: %s' % (slug+'-1',)
            ))
        return slug


class AudiosetUpdateForm(forms.ModelForm):

    class Meta:
        model = antropoloops_models.Audioset
        fields = [
            'image',
            'readme',
            'mode_display',
            'background',
            'map_scale',
            'map_center_x',
            'map_center_y'
        ]
        widgets = {
            'image' : ImagePreviewWidget(
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

    def clean_key(self):
        audioset_tracks = self.instance.track.first().audioset.tracks.all()
        current_key = self.instance.key
        keys    = list( antropoloops_models.Clip.objects.filter(track__in=audioset_tracks).values_list('key', flat=True) )
        if current_key in keys:
            keys.remove(current_key)
        new_key = self.cleaned_data['key']
        if new_key and new_key in keys:
            current_keys = reduce(lambda a, b : ("'%s' '%s'")%(a, b), keys)
            raise forms.ValidationError(
                _("La tecla '%s' ya está seleccionada. Teclas seleccionadas actualmente: %s" % ( new_key, current_keys ))
            )
        return new_key

    class Meta:
        model = antropoloops_models.Clip
        fields = '__all__'
