# django
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Publishable(models.Model):
    """ An abstract class to represent publishable content with its
        meta fields. """

    slug = models.SlugField(
        _('Slug'),
        blank=True
    )
    creation_date = models.DateField(
        _('Fecha de creación'),
        default=timezone.now
    )
    update_date = models.DateField(
        _('Última modificación'),
        auto_now=True,
    )
    published = models.BooleanField(
        _('Público'),
        blank=True,
        default=False,
    )
    owner = models.ForeignKey(
        User,
        verbose_name=_('Propietario'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        abstract = True
