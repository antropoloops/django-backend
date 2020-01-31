# django
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
# contrib
from adminsortable import admin as sortable
# project
from . import models

# Declare modeladmins

class AlbumAdmin(admin.ModelAdmin):
    model = models.Album

class AudioAdmin(admin.ModelAdmin):
    model = models.Audio

class ClipAdmin(admin.ModelAdmin):
    model = models.Clip

class TrackAdmin(admin.ModelAdmin):
    model = models.Track

class TrackInlineAdmin(sortable.SortableStackedInline):
    model = models.Track
    fields = [ 'name', ]
    extra = 0

class AudiosetAdmin(sortable.NonSortableParentAdmin):
    """TODO: require conditionally fields in display fieldset"""

    model = models.Audioset
    list_display = (
        'name',
        'description',
        'creation_date',
        'update_date',
        'slug',
        'mode_display'
    )
    fieldsets = (
        (None, {
            'fields' : (
                'name',
                'slug'
            )
        }),
        (_('Metadatos'), {
            'fields' : (
                'description',
                'readme',
                # TODO: add logo
            )
        }),
        (_('Visuales'), {
            'classes' : ( 'fieldset--display', ),
            'fields' : (
                'mode_display',
                # TODO: add background
                'map_url',
                'map_lambda',
                'map_shift_vertical',
                'map_scale',
                'map_center_x',
                'map_center_y'
            )
        }),
        (_('Audio'), {
            'fields' : (
                # TODO: add playmode
                'audio_bpm',
                'audio_quantize',
            )
        }),
    )
    inlines = [ TrackInlineAdmin, ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        super().save_model(request, obj, form, change)

    class Media:
        js = ('models/js/modeladmin_audioset.js',)

# Register model admins

admin.site.register(models.Album, AlbumAdmin)
admin.site.register(models.Audio, AudioAdmin)
admin.site.register(models.Clip, ClipAdmin)
admin.site.register(models.Track, TrackAdmin)
admin.site.register(models.Audioset, AudiosetAdmin)
