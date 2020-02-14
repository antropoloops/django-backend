# django
from django import template
from django.conf.urls.static import static
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def logo(set):
    field_exists = hasattr(set, 'logo')
    default_img_url = settings.STATIC_URL + 'dashboard/img/blank-image.svg'
    if field_exists and set.logo:
        return mark_safe(
            '<img src="{0}" alt="{1}" />'.format(
                set.logo.url,
                _('Logo del audioset')
            )
        )
    return mark_safe(
        '<img class="blank-image" src="{0}" alt="{1}" />'.format(
            default_img_url,
            _('Imagen genérica')
        )
    )

@register.filter
def description(set):
    blank_description =  '<p class="blank-description">{0}</p>'.format(
        _('Este elemento no aporta descripción')
    )
    return set.description if set.description else mark_safe(blank_description)
