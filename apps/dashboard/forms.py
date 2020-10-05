# python
from functools import reduce
# django
from django import forms
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _
from django.forms.models import inlineformset_factory
from django.core.exceptions import ValidationError
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.urls import reverse_lazy
# app
from apps.models import models
from apps.limited_textarea_widget.widgets import LimitedTextareaWidget
from apps.image_preview_widget.widgets import ImagePreviewWidget
from apps.autoslug_widget.widgets import AutoslugWidget

def namedWidget(input_name, widget=forms.CharField):
    if isinstance(widget, type):
        widget = widget()
    render = widget.render
    widget.render = lambda name, value, attrs=None, renderer=None: render(input_name, value, attrs, renderer)
    return widget


class ProjectForm(forms.ModelForm):

    slug = forms.SlugField(
        label=_('Ruta'),
        help_text=_(
            'Este campo contiene el fragmento final de la URL del proyecto'
        ),
        widget=AutoslugWidget(src='name')
    )

    class Meta:
        model = models.Project
        fields = [
            'name',
            'published',
            'description',
            'image',
            'readme',
            'slug',
        ]
        widgets = {
            'image' : ImagePreviewWidget(),
            'description' : LimitedTextareaWidget(attrs={'rows':2 }, limit=70),
        }

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if models.Project.objects.filter(
            slug=slug,
        ).exclude(
            pk=self.instance.pk
        ).exists():
            raise ValidationError(_(
                'Ya existe un proyecto con esa ruta. Por favor, '
                'cámbiala ligeramente. Por ejemplo: %s' % (slug+'-1',)
            ))
        return slug


class AudiosetForm(forms.ModelForm):

    slug = forms.SlugField(
        label=_('Ruta'),
        help_text=_(
            'Esta campo contiene el fragmento final de la URL del proyecto'
        ),
        widget=AutoslugWidget(src='name')
    )

    def __init__(self, *args, **kwargs):
        super(AudiosetForm,self).__init__(*args, **kwargs)
        self.fields['published'].help_text = _(
            'Cuando tengas listo tu audioset, marca esta casilla para '
            'aparezca en el índice del apartado «Comunidad».'
        )


    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if models.Audioset.objects.filter(
            slug=slug,
        ).exclude(
            pk=self.instance.pk
        ).exists():
            raise ValidationError(_(
                'Ya existe un audioset con esa ruta. Por favor, '
                'cámbiala ligeramente. Por ejemplo: %s' % (slug+'-1',)
            ))
        return slug

    class Meta:
        model = models.Audioset
        fields = [
            'name',
            'published',
            'description',
            'slug',
            'image',
            'readme',
            'mode_display',
            'background',
            'map_scale',
            'map_center_x',
            'map_center_y',
            'playmode',
            'audio_bpm',
            'audio_quantize',
            'map_url',
            'map_lambda',
            'map_shift_vertical',
        ]
        widgets = {
            'description' : LimitedTextareaWidget(attrs={'rows':2 }, limit=70),
            'image' : ImagePreviewWidget(
                placeholder=_('<img src="%s" />' % static('img/audioset.jpg'))
            ),
            'mode_display' : widgets.RadioSelect(),
            'background' : ImagePreviewWidget(),
        }

class TrackForm(forms.ModelForm):
    class Meta:
        model = models.Track
        fields = [
            'name',
            'volume',
            'color',
        ]


class TrackFormAjax(forms.ModelForm):

    class Meta:
        model = models.Track
        fields = [
            'name',
            'volume',
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
        model = models.Track
        fields = [
            'name',
            'volume',
            'color',
            'audioset'
        ]
        widgets = {
            'audioset' : widgets.HiddenInput()
        }

class Fieldset(object):
  def __init__(self, form, title, fields, classes):
    self.form = form
    self.title = title
    self.fields = fields
    self.classes = classes

  def __iter__(self):
    for field in self.fields:
      yield field


class ClipForm(forms.ModelForm):

    class Meta:
        model = models.Clip
        exclude = [
            'image_alt', 'audio_mp3', 'audio_ogg'
        ]
        widgets = {
            'image' : ImagePreviewWidget(placeholder='<img src="%s" />' % static('img/clip.jpg')),
        }

    def __init__(self, *args, **kwargs):
        super(ClipForm,self).__init__(*args, **kwargs)
        if len(args) > 0:
            self.track_pk = args[0].get('track')
        if 'initial' in kwargs:
            audioset_pk = kwargs['initial'].get('audioset')
            audioset = models.Audioset.objects.get(pk=audioset_pk)
            if audioset.mode_display == '2':
                self.fields['pos_x'].label = _('Longitud')
                self.fields['pos_x'].help_text = _(
                    'Longitud geográfica donde situar el clip. '
                    'Puedes usar el localizador situado en la parte superior del mapa '
                    'para rellenar automáticamente este campo'
                )
                self.fields['pos_y'].label = _('Latitud')
                self.fields['pos_y'].help_text = _(
                    'Latitud geográfica donde situar el clip. '
                    'Puedes usar el localizador situado en la parte superior del mapa '
                    'para rellenar automáticamente este campo'
                )

    def clean(self):
        cleaned_data = super().clean()
        if not 'pos_x' in cleaned_data or not 'pos_y' in cleaned_data or not cleaned_data['pos_x'] or not cleaned_data['pos_y']:
            raise forms.ValidationError(
                _("Es necesario especificar una posición para el clip")
            )
        return cleaned_data

    def clean_key(self):
        new_key = self.cleaned_data['key']
        if new_key:
            audioset_tracks = self.instance.track.first().audioset.tracks.all()
            keys = list( models.Clip.objects.filter(
                track__in=audioset_tracks,
                key__isnull=False
            ).values_list(
                'key',
                flat=True
            ))
            current_key = self.instance.key
            if current_key and current_key in keys:
                keys.remove(current_key)
            if new_key in keys:
                current_keys = reduce(lambda a, b : ("%s %s")%(a, b), keys)
                raise forms.ValidationError(
                    _("La tecla '%s' ya está seleccionada. Teclas seleccionadas actualmente: %s" % ( new_key, current_keys ))
                )
        return new_key


class ClipUpdateForm(ClipForm):

    pk = forms.IntegerField(
        widget=widgets.HiddenInput()
    )
