# django
from django import template
from django.conf.urls.static import static
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def blank_image():
    return mark_safe(
        '<img class="blank-image" src="{0}" alt="{1}" />'.format(
            settings.STATIC_URL + 'dashboard/img/blank-image.svg',
            _('Imagen genérica')
        )
    )

@register.filter
def description(set):
    blank_description =  '<p class="blank-description">{0}</p>'.format(
        _('Este elemento no aporta descripción')
    )
    return set.description if set.description else mark_safe(blank_description)
