# django
from django import forms
from apps.models import models as antropoloops_models
from apps.limited_textarea_widget.widgets import LimitedTextareaWidget

class AudiosetCreateForm(forms.ModelForm):

    class Meta:
        model = antropoloops_models.Audioset
        fields = [
            'name',
            'description',
            'mode_display'
        ]
        widgets = {
            'description' : LimitedTextareaWidget(limit=280),
        }
