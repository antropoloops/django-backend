# Expire page from cache
# https://stackoverflow.com/questions/2268417/expire-a-view-cache-in-django

# django
from django.core.cache import cache
from django.http import HttpRequest
from django.utils.cache import get_cache_key
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
# project
from . import models

def expire_page(path):
    request = HttpRequest()
    request.path = path
    request.META = {
        'SERVER_NAME' : 'play-admin.antropoloops.com',
        'SERVER_PORT' : '8000'
    }
    key = get_cache_key(request)
    if cache.has_key(key):
        cache.delete(key)

@receiver(post_save, sender=models.Project)
def expire_project_cache(sender, instance, **kwargs):
    if not instance.published:
        path = reverse(
            'api:resource', 
            kwargs={ 
                'slug' : instance.slug 
            }
        )
        expire_page(path)

