"""antropoloops URL Configuration"""

# django
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy
# project
from apps.registration import urls as registration_urls
from apps.dashboard import urls as dashboard_urls

urlpatterns = [
    # URLS related to user actions (login, password change, etc.)
    path('', include(registration_urls)),
    # django default admin urls
    path('admin/', admin.site.urls),

    # PAGES
    # URLS related to user dashboard (audiosets view, forms, etc.)
    path('', include(dashboard_urls)),
    # front
    path('', RedirectView.as_view(url='dashboard')),
]

# Add static URLS when running a standalone server through manage.py
if settings.DEBUG == True:
   urlpatterns += static( settings.STATIC_URL, document_root = settings.STATIC_ROOT )
   urlpatterns += static( settings.MEDIA_URL,  document_root = settings.MEDIA_ROOT )
