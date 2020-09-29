# django
from django import template
from django.utils.safestring import mark_safe
# project
from apps.textblock.models import Textblock
register = template.Library()

@register.simple_tag
def textblock(slug):
    try:
        block = Textblock.objects.get(slug = slug)
        return mark_safe(
            "<div class='textblock'><div class='textblock__inner'>%s</div></div>" % block.body
        )
    except:
        return None
