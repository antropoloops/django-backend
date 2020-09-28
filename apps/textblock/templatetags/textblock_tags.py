# django
from django import template
from django.utils.safestring import mark_safe
# project
from apps.textblock.models import Textblock
register = template.Library()

@register.simple_tag
def textblock(slug):
    block = Textblock.objects.get(slug=slug)
    return mark_safe( block.body )
