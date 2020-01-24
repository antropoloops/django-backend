# django
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils.text import slugify
# contrib
from colorfield.fields import ColorField
from django_countries.fields import CountryField
from adminsortable.models import SortableMixin
# project
from .abstract.publishable import Publishable
from . import categories
from . import validators


class Album(models.Model):
    """ Album model definition """

    name = models.CharField(
        _('Nombre del álbum'),
        max_length=128,
        blank=False,
    )
    artist = models.CharField(
        _('Nombre del artista'),
        max_length=128,
        blank=False,
    )
    year = models.PositiveSmallIntegerField(
        _('Año de lanzamiento'),
        blank=True,
        validators=[ validators.album_year_validator ]
    )
    country = CountryField(
        _('País'),
        blank=True,
    )
    # TODO: cover #

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Álbum')
        verbose_name_plural = _('Álbumes')


class Audio(models.Model):
    """ Audio model definition """

    name = models.CharField(
        _('Nombre del audio'),
        max_length=128,
        blank=False,
    )
    album = models.ForeignKey(
        Album,
        blank=True,
        null=True,
        verbose_name=_('Álbum'),
        on_delete=models.SET_NULL,
    )
    #TODO: audio_mp3
    #TODO: audio_ogg
    #TODO: audio_wav
    beats = models.PositiveSmallIntegerField(
        _('Beats'),
        default=0
    )
    volume = models.PositiveSmallIntegerField(
        _('Volumen'),
        default=0,
    )

    def __str__(self):
        return self.name


class Clip(models.Model):
    """ Clip model definition """

    name = models.CharField(
        _('Nombre del clip'),
        max_length=128,
        blank=True,
        help_text=_(
            'Si este campo se deja vacío se usará el nombre '
            'de la canción relacionada'
        )
    )
    artist = models.CharField(
        _('Nombre del artista'),
        max_length=128,
        blank=True,
        help_text=_(
            'Si este campo se deja vacío se usará el artista '
            'del audio relacionado'
        )
    )
    place = models.CharField(
        _('Lugar'),
        max_length=128,
        blank=True,
    )
    #TODO: cover
    audio = models.ForeignKey(
        Audio,
        _('Audio'),
    )
    readme = models.TextField(
        _('Notas adicionales'),
        blank=True,
    )
    key = models.CharField(
        _('Tecla'),
        max_length=1,
        blank=True,
    )
    pos_x = models.IntegerField(
        _('Coordenada X'),
        default = 0,
        blank=True,
    )
    pos_y = models.IntegerField(
        _('Coordenada Y'),
        default = 0,
        blank=True,
    )

    def __str__(self):
        return self.name if self.name else self.audio.name


class Audioset(Publishable):
    """ Audioset model definition """

    name = models.CharField(
        _('Nombre del set'),
        max_length=128,
        blank=False,
    )
    slug = models.SlugField(
        _('Ruta'),
        blank=True,
        help_text=_(
            'Ruta del audioset. Si se deja vacío este campo '
            'se creará de manera automática a partir del nombre del set.'
        )
    )
    description = models.TextField(
        _('Descripción corta'),
        blank=True,
        help_text=_(
            'Descripción corta. Se usará en vistas de contenido. '
        )
    )
    readme = models.TextField(
        _('Descripción'),
        max_length=128,
        blank=True,
        help_text=_(
            'Descripción larga. Se usará en la página específica '
            'del audioset.'
        )
    )
    #TODO: logo

    # Visual fieldset
    mode_display = models.CharField(
        _('Tipo de visual'),
        max_length=2,
        blank=False,
        default=1,
        choices=categories.VISUAL_DISPLAY_MODE,
    )
    #TODO: background
    map_url = models.URLField(
        _('URL del mapa'),
        blank=True,
    )
    map_lambda = models.IntegerField(
        _('Lambda'),
        default=0,
        blank=True,
    )
    map_shift_vertical = models.IntegerField(
        _('Desplazamiento vertical del mapa'),
        default=0,
        blank=True,
    )
    map_scale = models.IntegerField(
        _('Escala del mapa'),
        default=1,
        blank=True,
    )
    map_center_x = models.IntegerField(
        _('Coordenada X del centro del mapa'),
        default=0,
        blank=True,
    )
    map_center_y = models.IntegerField(
        _('Coordenada Y del centro del mapa'),
        default=0,
        blank=True,
    )

    # Audio fieldset
    #TODO: playmode
    audio_bpm = models.PositiveSmallIntegerField(
        _('BPM'),
        default=120,
    )
    audio_quantize = models.PositiveSmallIntegerField(
        _('Quantize'),
        default=0,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Populate automatically 'slug' field"""
        if not self.id and not self.slug:
            self.slug = slugify(self.name)
        super(Audioset, self).save(*args, **kwargs)


class Track(SortableMixin):
    """ Track model definition """

    name = models.CharField(
        _('Nombre del track'),
        max_length=128,
        blank=False,
    )
    position = models.PositiveSmallIntegerField(
        _('Posición'),
        default=0,
        blank=False,
        editable=False,
        db_index=True,
    )
    volume = models.PositiveSmallIntegerField(
        _('Volumen'),
        default=0
    )
    color = ColorField(
        _('Color'),
        default='#ffffff',
        blank=True
    )
    clips = models.ManyToManyField(
        Clip,
        verbose_name=_('Clips'),
    )
    audioset = models.ForeignKey(
        Audioset,
        null=True,
        verbose_name=_('Audioset'),
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('position',)

    def __str__(self):
        return self.name
