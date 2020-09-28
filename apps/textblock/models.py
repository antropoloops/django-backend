# django
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
# contrib
from ckeditor_uploader.fields import RichTextUploadingField


class Textblock(models.Model):
    """ Text blocks """

    label = models.CharField(
        _('Label'),
        blank=False,
        null=True,
        help_text=_(
            'Etiqueta del bloque de texto. '
        ),
        max_length=256
    )
    slug = models.CharField(
        _('Slug'),
        blank=True,
        max_length=256
    )
    body = RichTextUploadingField(
        _('Cuerpo de texto'),
        blank=False,
        null=True,
        help_text=_(
            'Cuerpo de texto'
        )
    )

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        """Populate automatically 'slug' field"""
        if not self.id:
            self.slug = slugify(self.label)
        super(Textblock, self).save(*args, **kwargs)
