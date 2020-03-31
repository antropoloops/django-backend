# python
import os.path
# django
from django import template
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.middleware.csrf import get_token
# project
from django.conf import settings

register = template.Library()

@register.simple_tag
def css(file):
    return  settings.STATIC_URL + 'css/' + file + '.css'

@register.simple_tag
def js(file):
    return  settings.STATIC_URL + 'js/' + file + '.js'

@register.simple_tag
def img(file):
    return  settings.STATIC_URL + 'img/' + file

@register.simple_tag
def csrf(req):
    return get_token(req)
