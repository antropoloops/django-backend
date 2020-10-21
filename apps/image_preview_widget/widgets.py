# django
from django import forms
from django.template.loader import render_to_string

class CustomFileInput(forms.widgets.ClearableFileInput):
    template_name = 'custom-file-input.html'

class ImagePreviewWidget(CustomFileInput):
    """A custom widget, to preview video iframes from an external service as vimeo or youtube"""

    class Media:
         """Bind static assets to widget rendering"""
         js = ('image_preview_widget/js/imagePreview.js',)

    def __init__(self, attrs=None, placeholder=None):
        self.placeholder = placeholder
        super(ImagePreviewWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        """Render widget"""

        parent_widget = super(ImagePreviewWidget, self).render(name, value, attrs )
        picture_preview = render_to_string("image-preview-widget.html", {
            'id'            : attrs['id'],
            'parent_widget' : parent_widget,
            'value'         : value,
            'placeholder'   : self.placeholder
        })
        return picture_preview
