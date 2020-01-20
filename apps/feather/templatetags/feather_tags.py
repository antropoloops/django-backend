# django
from django import template

register = template.Library()

@register.inclusion_tag('icon.html')
def icon(name):
    return {
        'name' : name
    }
