# django
from django import template

register = template.Library()

@register.filter(name='check_file')
def check_file(value):
    return value and os.path.isfile(settings.MEDIA_ROOT + "/" + value.name)
