# django
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
# contrib
from colorful.fields import RGBColorField
from django_countries.fields import CountryField
from adminsortable.models import SortableMixin
from ckeditor_uploader.fields import RichTextUploadingField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
# project
from .abstract.publishable import Publishable
from . import categories
from . import validators

validator_mp3 = validators.AudioTypeValidator(["audio/mpeg"])
validator_ogg = validators.AudioTypeValidator(["audio/ogg"])
validator_wav = validators.AudioTypeValidator(["audio/wav"])

class Clip(models.Model):
    """ Clip model definition """

    order = models.PositiveSmallIntegerField(
        _('Orden'),
        default=0,
        blank=False,
        editable=False,
        db_index=True,
    )
    name = models.CharField(
        _('Nombre del clip'),
        max_length=128,
        blank=False,
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
    image = models.ImageField(
        _('Imagen representativa'),
        blank=True,
        upload_to='images/clips'
    )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[
            ResizeToFill(100, 50)
        ],
        format='JPEG',
        options={
            'quality': 60
        }
    )
    audio_name = models.CharField(
        _('Nombre del audio'),
        max_length=128,
        blank=False,
        null=True,
    )
    audio_mp3 = models.FileField(
        _('Archivo de audio MP3'),
        blank=True,
        validators=[ validator_mp3 ],
        upload_to='audio/mp3',
        help_text=_(
            'Archivo de audio del sample en formato MP3'
        )
    )
    audio_ogg = models.FileField(
        _('Archivo de audio OGG'),
        blank=True,
        validators=[ validator_ogg ],
        upload_to='audio/ogg',
        help_text=_(
            'Archivo de audio del sample en formato OGG'
        )
    )
    audio_wav = models.FileField(
        _('Archivo de audio MP3'),
        blank=True,
        validators=[ validator_wav ],
        upload_to='audio/wav',
        help_text=_(
            'Archivo de audio del sample en formato WAV'
        )
    )
    artist = models.CharField(
        _('Nombre del artista'),
        max_length=128,
        blank=True,
    )
    year = models.PositiveSmallIntegerField(
        _('Año'),
        blank=True,
        null=True,
        validators=[ validators.album_year_validator ]
    )
    album_name = models.CharField(
        _('Nombre del álbum'),
        max_length=128,
        blank=True,
    )
    country = CountryField(
        _('País'),
        blank=True,
        blank_label=_('Escoge un pais')
    )
    place = models.CharField(
        _('Lugar'),
        max_length=128,
        blank=True,
    )
    pos_x = models.FloatField(
        _('Posición X'),
        default = 0,
        blank=False,
        help_text=_(
            'Coordinada horizontal de la posición del clip en la imagen'
        )
    )
    pos_y = models.FloatField(
        _('Posición Y'),
        default = 0,
        blank=False,
        help_text=_(
            'Coordinada vertical de la posición del clip en la imagen'
        )
    )
    beats = models.PositiveSmallIntegerField(
        _('Beats'),
        default=0
    )
    volume = models.PositiveSmallIntegerField(
        _('Volumen'),
        default=0,
    )

    def __str__(self):
        return self.name if self.name else self.audio.name

    @property
    def color(self):
        return self.track.first().color

    class Meta:
        ordering = ('track', 'order',)


class Project(Publishable):
    """ Project model definition """

    name = models.CharField(
        _('Nombre del proyecto'),
        max_length=128,
        blank=False,
    )
    description = models.TextField(
        _('Descripción corta'),
        blank=True,
        help_text=_(
            'Descripción corta. Se usará en vistas de contenido. '
        )
    )
    readme = RichTextUploadingField(
        _('Descripción'),
        max_length=128,
        blank=True,
        help_text=_(
            'Descripción larga. Se usará en la página específica '
            'del proyecto.'
        )
    )
    background = models.ImageField(
        _('Imagen de fondo'),
        blank=True,
        upload_to='images/projects',
        help_text=_(
            'Añade opcionalmente una imagen representativa. Ésta como fondo de '
            'la página específica del proyecto. '
        )
    )
    image = models.ImageField(
        _('Imagen representativa'),
        blank=True,
        upload_to='images/projects',
        help_text=_(
            'Añade opcionalmente una imagen representativa. Ésta se usará en la '
            ' vista de proyectos. '
        )
    )
    users = models.ManyToManyField(
        User,
        verbose_name=_('Usuarias'),
        related_name='projects',
        blank=True,
        help_text=_(
            'Usuarias con permisos dentro de este proyecto'
        )
    )

    def __str__(self):
        return self.name


class Audioset(Publishable):
    """ Audioset model definition """

    name = models.CharField(
        _('Nombre del set'),
        max_length=128,
        blank=False,
        help_text=_(
            'Elige un nombre para el audioset.'
        )
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
    readme = RichTextUploadingField(
        _('Descripción'),
        max_length=128,
        blank=True,
        help_text=_(
            'Descripción larga. Se usará en la página específica '
            'del audioset.'
        )
    )
    project = models.ForeignKey(
        Project,
        verbose_name=_('Proyecto'),
        related_name='audiosets',
        null=True,
        on_delete=models.CASCADE,
        help_text=_(
            'Proyecto al que pertenece el audioset'
        )
    )
    image = models.ImageField(
        _('Logo'),
        blank=True,
        upload_to='images/audiosets'
    )

    # Visual fieldset
    mode_display = models.CharField(
        _('Tipo de visual'),
        max_length=2,
        blank=True,
        null=False,
        default='',
        choices=categories.VISUAL_DISPLAY_MODE,
        help_text=_(
            'Elige el modo en que quieres mostrar el audioset. Elige <em>panel</em> '
            'si quieres mostrar los distintos clips sobre una imagen de fondo. '
            'Elige <em>mapa</em> si quieres localizarlos sobre un mapa. '
        )
    )
    background = models.ImageField(
        _('Background'),
        blank=True,
        upload_to='images/backgrounds'
    )
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
    map_scale = models.FloatField(
        _('Escala del mapa'),
        default=250,
        blank=True,
    )
    map_center_x = models.FloatField(
        _('Coordenada X del centro del mapa'),
        default=0,
        blank=True,
    )
    map_center_y = models.FloatField(
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

    @property
    def is_panel(self):
        return self.mode_display=='1'

    def __str__(self):
        return self.name


class Track(SortableMixin):
    """ Track model definition """

    name = models.CharField(
        _('Nombre del track'),
        max_length=128,
        blank=False,
    )
    order = models.PositiveSmallIntegerField(
        _('Orden'),
        default=0,
        blank=False,
        editable=False,
        db_index=True,
    )
    volume = models.PositiveSmallIntegerField(
        _('Volumen'),
        default=0
    )
    color = RGBColorField(
        _('Color'),
        blank=True
    )
    clips = models.ManyToManyField(
        Clip,
        verbose_name=_('Clips'),
        related_name='track'
    )
    audioset = models.ForeignKey(
        Audioset,
        null=True,
        verbose_name=_('Audioset'),
        related_name='tracks',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.name

class Theme(models.Model):

    name = models.CharField(
        _('Nombre del tema'),
        max_length=128,
        blank=False,
    )
    description = RichTextUploadingField(
        _('Descripción'),
        max_length=128,
        blank=True,
        help_text=_(
            'Descripción larga. Se usará en la página específica '
            'del audioset.'
        )
    )
    slug = models.SlugField(
        _('Ruta'),
        blank=True,
        help_text=_(
            'Ruta del tema. Si se deja vacío este campo '
            'se creará de manera automática a partir del nombre del set.'
        )
    )
    order = models.PositiveSmallIntegerField(
        _('Orden'),
        default=0,
        blank=False,
        editable=False,
        db_index=True,
    )

    class Meta:
        verbose_name = _('tema didáctico')
        verbose_name_plural = _('temas didácticos')
        ordering = ('order',)

    def __str__(self):
        return self.name


class ThemeUnit(SortableMixin):

    project = models.ForeignKey(
        Project,
        verbose_name = _(
            'Proyecto que compone la unidad'
        ),
        related_name = 'project_units',
        on_delete = models.SET_NULL,
        null = True,
        blank = True
    )
    set = models.ForeignKey(
        Audioset,
        verbose_name=_(
            'Set que compone la unidad'
        ),
        related_name = 'set_units',
        on_delete = models.SET_NULL,
        blank = True,
        null = True,
    )

    theme = models.ForeignKey(
        Theme,
        verbose_name=_(
            'Tema'
        ),
        related_name='units',
        on_delete = models.CASCADE,
        null=True,
        blank=False
    )
    order = models.PositiveSmallIntegerField(
        _('Orden'),
        default=0,
        blank=False,
        editable=False,
        db_index=True,
    )

    class Meta:
        verbose_name = _('unidad didáctica')
        verbose_name_plural = _('unidades didácticas')
        ordering = ('order',)

    def __str__(self):
        return 'Unidad %s' % self.order
