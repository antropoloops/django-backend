# django
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
# contrib
from adminsortable import admin as sortable
from django.core.exceptions import ValidationError
from django import forms
# project
from . import models

# Declare modeladmins

class ClipAdmin(admin.ModelAdmin):
    model = models.Clip

class TrackAdmin(admin.ModelAdmin):
    model = models.Track

class TrackInlineAdmin(sortable.SortableStackedInline):
    model = models.Track
    fields = [ 'name', ]
    extra = 0

class ProjectAdmin(admin.ModelAdmin):
    model = models.Project
    fields = (
        ('name', 'slug',),
        'owner',
        'users',
        'image',
        'published'
    )

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
                'image',
                'project',
                'slug',
                'owner',
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
                'background',
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

class ThemeUnitForm(forms.ModelForm):
    model  = models.ThemeUnit
    fields = (('set', 'project'),)

    def clean(self):
        if not self.cleaned_data['set'] and not self.cleaned_data['project']:
            raise ValidationError(_(
                'Tiene que haber una referencia a un elemento, sea un Audioset o un Proyecto'
            ))
        if self.cleaned_data['set'] and self.cleaned_data['project']:
            raise ValidationError(_(
                'Una unidad se compone de un único elemento, quita una de las referencias'
            ))
        return self.cleaned_data


class ThemeUnitAdmin(sortable.SortableStackedInline):

    model  = models.ThemeUnit
    extra  = 0
    form = ThemeUnitForm
    fields = (('set', 'project'),)

class ThemeAdmin(sortable.NonSortableParentAdmin):
    model   = models.Theme
    inlines = [ ThemeUnitAdmin ]

# Register model admins

admin.site.register(models.Clip, ClipAdmin)
admin.site.register(models.Track, TrackAdmin)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Audioset, AudiosetAdmin)
# admin.site.register(models.ThemeUnit, admin.ModelAdmin)
admin.site.register(models.Theme, ThemeAdmin)
