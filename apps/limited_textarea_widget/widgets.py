# django
from django import forms
from django.template.loader import render_to_string


class LimitedTextareaWidget(forms.widgets.Textarea):
    """ Textarea widget with a max number of characters """

    def __init__(self, attrs=None, limit=500):
        self.limit = limit
        super(LimitedTextareaWidget, self).__init__(attrs)

    class Media:
        """Bind static assets to widget rendering"""
        js = ('limited_textarea_widget/js/limited_textarea.js',)

    def render(self, name, value, attrs=None, renderer=None):
        """Render widget"""
        attrs['maxlength'] = self.limit
        parent_widget = super(LimitedTextareaWidget, self).render(name, value, attrs)
        limited_textarea_widget = render_to_string("limited-textarea-widget.html",
        {
            'parent_widget': parent_widget,
            'limit' : self.limit,
        })
        return limited_textarea_widget
