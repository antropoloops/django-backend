# django
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.core import serializers
# app
from apps.dashboard import forms
from apps.models import models


def track(request):
    """ Get Track object. """

    if request.is_ajax and request.user.is_authenticated:
        pk = request.GET['pk']
        track = models.Track.objects.get(pk=pk)
        return JsonResponse(
            serializers.serialize(
                'json',
                [track],
                fields=(
                    'name',
                    'color',
                )
            ),
            safe=False
        )
    else:
        return HttpResponse(
            "Forbidden"
        )

@csrf_protect
def track_create(request):
    """ Creates a Track object. """

    if request.method == 'POST' and request.is_ajax and request.user.is_authenticated:
        data = request.POST
        print(data)
        form = forms.TrackFormAjax(data)
        if form.is_valid():
            new_track = form.save()
            return HttpResponse(
                _("El track %s ha sido creado con éxito" % new_track.pk )
            )
        print(form.errors)
        return HttpResponse(
            form.errors
        )
    else:
        return HttpResponse(
            "Forbidden"
        )

@csrf_protect
def track_update(request):
    """ Creates a Track object. """

    if request.method == 'POST' and request.is_ajax and request.user.is_authenticated:
        data = request.POST
        instance = models.Track.objects.get(pk=data['pk'])
        form = forms.TrackUpdateFormAjax(
            data,
            instance=instance
        )
        if form.is_valid():
            form.save()
            return HttpResponse(
                _( "El track ha sido editado con éxito" )
            )
        print(form.errors)
        return HttpResponse(
            _( "El formulario no es válido" )
        )
    else:
        return HttpResponse(
            "Forbidden"
        )


@csrf_protect
def track_delete(request):
    """ Creates a Track object. """

    if request.method == 'POST' and request.is_ajax and request.user.is_authenticated:
        pk = request.POST['pk']
        models.Track.objects.get(pk=pk).delete()
        return HttpResponse(
            _( "El track %s ha sido borrado con éxito" % pk )
        )
    else:
        return HttpResponse(
            "Forbidden"
        )

def clip(request):
    """ Get Clip object. """

    if request.is_ajax and request.user.is_authenticated:
        pk = request.GET['pk']
        clip = models.Clip.objects.get(pk=pk)
        return JsonResponse(
            serializers.serialize(
                'json',
                [clip],
            ),
            safe=False
        )
    else:
        return HttpResponse(
            "Forbidden"
        )

@csrf_protect
def clip_create(request):
    """ Creates a Clip object. """

    if request.method == 'POST' and request.is_ajax and request.user.is_authenticated:
        data = request.POST
        print(data)
        form = forms.ClipFormAjax(data)
        if form.is_valid():
            track = models.Track.objects.get(pk=data['track'])
            new_clip = form.save()
            track.clips.add(new_clip)
            track.save()
            print(new_clip.track)
            return HttpResponse(
                _("El clip %s ha sido creado con éxito" % new_clip.pk )
            )
        print(form.errors)
        return HttpResponse( form.errors )
    else:
        return HttpResponse(
            "Forbidden"
        )

@csrf_protect
def clip_update(request):
    """ Creates a Clip object. """

    if request.method == 'POST' and request.is_ajax and request.user.is_authenticated:
        data = request.POST
        print(data)
        clip = models.Clip.objects.get(pk=data['pk'])
        clipform = forms.ClipUpdateFormAjax(data, instance=clip)
        if clipform.is_valid():
            print('%s guardado' % clip.name)
            clipform.save()
        else:
            return HttpResponse(clipform.errors)
        return HttpResponse(
            _( "El clip ha sido editado con éxito" )
        )
    else:
        return HttpResponse(
            "Forbidden"
        )


@csrf_protect
def clip_delete(request):
    """ Creates a Clip object. """

    if request.method == 'POST' and request.is_ajax and request.user.is_authenticated:
        pk = request.POST['pk']
        print(request.POST)
        models.Clip.objects.get(pk=pk).delete()
        return HttpResponse(
            _( "El clip %s ha sido borrado con éxito" % pk )
        )
    else:
        return HttpResponse(
            "Forbidden"
        )
