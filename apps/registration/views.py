# django
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

def password_reset_done(request):
    messages.success(
        request,
        _(
            'Te hemos enviado instrucciones para cambiar tu contraseña a '
            'tu correo electrónico. Si no las encuentras comprueba '
            'que el correo introducido se corresponde al de tu usuari@ y '
            'revisa la bandeja de spam. '
        )
    )
    return HttpResponseRedirect( reverse('login'))

def password_reset_complete(request):
    messages.success(
        request,
        _(
            'Has cambiado tu contraseña con éxito. '
            'Ahora puedes hacer login en la plataforma'
        )
    )
    return HttpResponseRedirect( reverse('login'))


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]

    def __init__(self, *args, **kwargs):
        super(UserForm,self).__init__(*args, **kwargs)
        self.fields['username'].help_text = _(
            'Tienes un límite de 150 caracteres. Sólo puedes emplear letras, '
            'números y los caracteres especiales "@", ".", "+", "-" y "_"'
        )
        self.fields['username'].label = 'Nombre de usuario'
        self.fields['email'].label = 'Correo electrónico'


class Profile(UpdateView):

    form_class = UserForm
    template_name = 'registration/userform.html'
    success_url = reverse_lazy('audioset_list')

    def get_object(self, queryset=None, *args, **kwargs):
        return self.request.user
