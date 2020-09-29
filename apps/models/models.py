# django
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
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
validator_wav = validators.AudioTypeValidator([
    "audio/wav",
    "audio/x-wav",
    "audio/x-wave",
    "audio/vnd.wave"
])
validator_audio = validators.AudioTypeValidator([
    "audio/mpeg",
    "audio/ogg"
    "audio/wav",
    "audio/x-wav",
    "audio/x-wave",
    "audio/vnd.wave"
])

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
        help_text=_(
            'Es el nombre que se muestra en tu clip antes de activarlo. '
            'Úsalo para describir qué es...por ejemplo «ritmo base» o «sonido calle»…'
        )
    )
    readme = RichTextUploadingField(
        _('Notas adicionales'),
        blank=True,
        help_text=_(
            'Aquí puedes insertar texto, imágenes y contenido para explicar más '
            'cosas del audio. Por ejemplo puedes insertar un link a otra página '
            'donde se pueda oir completo el audio o contar alguna historia sobre '
            'el mismo.'
        )
    )
    key = models.CharField(
        _('Tecla'),
        max_length=1,
        blank=True,
    )
    image = models.ImageField(
        _('Imagen'),
        blank=True,
        upload_to='images/clips/',
        help_text=_(
            'Sube una imagen cuadrada como portada de tu clip '
            '(mínimo e ideal 400x400 px).'
        )
    )
    image_small = ImageSpecField(
        source='image',
        processors=[
            ResizeToFill(400, 400)
        ],
        format='JPEG',
        options={
            'quality': 90
        }
    )
    image_thumb = ImageSpecField(
        source='image',
        processors=[
            ResizeToFill(100, 100)
        ],
        format='JPEG',
        options={
            'quality': 90
        }
    )
    image_alt = models.ImageField(
        _('Imagen secundaria'),
        blank=True,
        upload_to='images/clips/',
    )
    image_alt_small = ImageSpecField(
        source='image_alt',
        processors=[
            ResizeToFill(400, 400)
        ],
        format='JPEG',
        options={
            'quality': 90
        }
    )
    image_alt_thumb = ImageSpecField(
        source='image_alt',
        processors=[
            ResizeToFill(100, 100)
        ],
        format='JPEG',
        options={
            'quality': 90
        }
    )
    audio_name = models.CharField(
        _('Nombre del audio'),
        max_length=128,
        blank=True,
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
        _('Archivo de audio'),
        blank=True,
        validators=[ validator_audio ],
        upload_to='audio/wav',
        help_text=_(
            'Archivo de audio del sample. Idealmente en WAV aunque acepta también '
            'formatos MP3 y OGG.'
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
        null=True,
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
            'Coordinada horizontal de la posición del clip en la imagen. '
            'Haz click en un punto de la imagen para rellenar este campo automáticamente.'
        )
    )
    pos_y = models.FloatField(
        _('Posición Y'),
        default = 0,
        blank=False,
        help_text=_(
            'Coordinada vertical de la posición del clip en la imagen. '
            'Haz click en un punto de la imagen para rellenar este campo automáticamente.'
        )
    )
    beats = models.PositiveSmallIntegerField(
        _('Beats'),
        default=0,
        blank=True,
        help_text=_(
            'Número de beats de los samples del clip'
        )
    )
    volume = models.FloatField(
        _('Volumen'),
        default=1,
        null=True,
        blank=True,
        help_text=_(
            'Ajuste de volumen para los samples del clip'
        )
    )

    def __str__(self):
        return self.name if self.name else self.audio_name

    @property
    def color(self):
        return self.track.first().color

    @property
    def audioset(self):
        track = self.track.first()
        return track.audioset.name if track else ''

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
        _('Imagen'),
        blank=True,
        upload_to='images/projects',
        help_text=_(
            'Añade opcionalmente una imagen representativa. Ésta se usará en la '
            ' vista de proyectos. '
        )
    )
    image_small = ImageSpecField(
        source='image',
        processors=[
            ResizeToFill(400, 400)
        ],
        format='JPEG',
        options={
            'quality': 90
        }
    )
    image_thumb = ImageSpecField(
        source='image',
        processors=[
            ResizeToFill(100, 100)
        ],
        format='JPEG',
        options={
            'quality': 90
        }
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
    in_home = models.BooleanField(
        _('Mostrar en la home'),
        blank=True,
        default=False
    )

    def is_owned_by(self, user):
        return user.is_staff or user == self.owner

    def __str__(self):
        return self.name

    @property
    def play_id(self):
        return 'p-%s' % self.pk


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
            'Este texto funciona como un subtítulo para tu audioset, puedes explicar muy brevemente qué es.'
        )
    )
    readme = RichTextUploadingField(
        _('Descripción'),
        blank=True,
        help_text=_(
            'Aquí puedes insertar texto, imágenes y contenido para explicar en qué '
            'contexto has realizado tu audioset, contar un poco del proyecto, etc.'
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
        _('Imagen'),
        blank=True,
        upload_to='images/audiosets',
        help_text=_(
            'Sube una imagen cuadrada como portada de tu audioset '
            '(mínimo e ideal 400x400 px).'
        )
    )
    image_small = ImageSpecField(
        source='image',
        processors=[
            ResizeToFill(400, 400)
        ],
        format='JPEG',
        options={
            'quality': 90
        }
    )
    image_thumb = ImageSpecField(
        source='image',
        processors=[
            ResizeToFill(100, 100)
        ],
        format='JPEG',
        options={
            'quality': 90
        }
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
        null=True,
        default='https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json',
        help_text=_(
            'Faltaría un texto que explique esto'
        )
    )
    map_lambda = models.IntegerField(
        _('Lambda del mapa'),
        default=0,
        blank=True,
        help_text=_(
            'Faltaría un texto que explique esto'
        )
    )
    map_shift_vertical = models.IntegerField(
        _('Desplazamiento vertical del mapa'),
        default=0,
        blank=True,
        help_text=_(
            'Faltaría un texto que explique esto'
        )
    )
    map_scale = models.FloatField(
        _('Escala del mapa'),
        default=1,
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

    playmode = models.CharField(
        _('Tipo de audioset'),
        default='0',
        choices=(
            ('0', _('Monofónico')),
            ('1', _('Polifónico')),
        ),
        max_length=1,
        null=False,
        help_text=_(
            'Monofónico: sólo puede sonar un audio a la vez. '
            'Polifónico: pueden sonar varios audios a la vez.'
        )
    )

    audio_bpm = models.PositiveSmallIntegerField(
        _('BPM del audio'),
        default=120,
        help_text=_(
            'BPM son las pulsaciones por minuto. Tienes que poner aquí el valor '
            'que hayas usado en tu software de edición para el audio. '
            '<a href="https://es.wikipedia.org/wiki/Pulsaciones_por_minuto" '
            'target="_blank">Más información</a>.'
        )
    )

    audio_quantize = models.PositiveSmallIntegerField(
        _('Quantize'),
        default=0,
        blank=True,
        null=True,
        help_text=_(
            'Faltaría un texto que explique esto'
        )
    )

    def is_owned_by(self, user):
        return user.is_staff or user == self.owner

    @property
    def is_panel(self):
        return self.mode_display=='1'

    @property
    def play_id(self):
        return 'a-%s' % self.pk

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
        default=1,
        blank=True,
        null=True,
        help_text=_(
            'Faltaría un texto que explique esto'
        )
    )
    color = RGBColorField(
        _('Color'),
        blank=False,
        default='#ffffff',
        colors=["#48f912", "#12f99d", "#f912e2", "#f9126b", "#12acf9", "#1276f9"],
        help_text=_(
            'Escoge el color de fondo de la pista, '
            'los clips que crees dentro de ella tendrán un color más claro '
            'que el que elijas.'
        )
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

    def delete(self, *args, **kwargs):
        self.clips.all().delete()
        super().delete()

    def __str__(self):
        return self.name


class Theme(models.Model):

    name = models.CharField(
        _('Nombre del tema'),
        max_length=128,
        blank=False,
    )
    description = models.TextField(
        _('Descripción corta'),
        blank=True,
        help_text=_(
            'Descripción corta. Se usará en vistas de contenido.'
        )
    )
    readme = RichTextUploadingField(
        _('Descripción'),
        blank=True,
        help_text=_(
            'Descripción larga. Se usará en la página específica '
            'del tema.'
        )
    )
    update_date = models.DateField(
        _('Última modificación'),
        auto_now=True,
    )
    image = models.ImageField(
        _('Imagen'),
        blank=True,
        upload_to='images/themes'
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
        verbose_name = _('tema')
        verbose_name_plural = _('temas')
        ordering = ('order',)

    def __str__(self):
        return self.name


class ThemeUnit(SortableMixin):

    project = models.ForeignKey(
        Project,
        verbose_name = _(
            'Proyecto relacionado'
        ),
        related_name = 'project_units',
        on_delete = models.SET_NULL,
        null = True,
        blank = True
    )
    set = models.ForeignKey(
        Audioset,
        verbose_name=_(
            'Set relacionado'
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
        verbose_name = _('contenido relacionado')
        verbose_name_plural = _('contenidos relacionados')
        ordering = ('order',)

    def __str__(self):
        return 'Contenido ' + str(self.order)
