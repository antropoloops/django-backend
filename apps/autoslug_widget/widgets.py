# django
from django import forms
from django.template.loader import render_to_string


class AutoslugWidget(forms.widgets.TextInput):
    """ Textarea widget with a max number of characters """

    def __init__(self, attrs=None, src='title'):
        self.src = src
        super(AutoslugWidget, self).__init__(attrs)

    class Media:
        """Bind static assets to widget rendering"""

        js = ('autoslug_widget/js/autoslug_widget.js',)

    def render(self, name, value, attrs=None, renderer=None):
        """Render widget"""

        attrs['data-autoslug-src'] = self.src
        parent_widget = super(AutoslugWidget, self).render(name, value, attrs)
        return parent_widget
