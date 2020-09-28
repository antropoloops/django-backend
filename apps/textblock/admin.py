# django
from django.contrib import admin
# project
from apps.textblock.models import Textblock

# Register your models here.
admin.site.register(Textblock, admin.ModelAdmin)
