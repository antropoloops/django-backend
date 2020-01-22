# django
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages

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
