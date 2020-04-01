# django
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.core import serializers
from .serializers import PropJsonSerializer
# contrib
from bulk_update.helper import bulk_update
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
    return HttpResponse(status=403)

def track_clips(request):
    """ Get Track clips. """

    if request.is_ajax and request.user.is_authenticated:
        pk = request.GET['pk']
        clips = models.Clip.objects.filter(track__audioset=pk)
        return JsonResponse(
            PropJsonSerializer().serialize(
                clips,
                fields=(
                    'name',
                    'pos_x',
                    'pos_y',
                ),
                props=(
                    'color',
                )
            ),
            safe=False
        )
    return HttpResponse(status=403)

@csrf_protect
def track_create(request):
    """ Creates a Track object. """

    if request.method == 'POST' and request.is_ajax and request.user.is_authenticated:
        data = request.POST
        form = forms.TrackFormAjax(data)
        if form.is_valid():
            new_track = form.save()
            return HttpResponse(
                _("El track %s ha sido creado con éxito" % new_track.pk )
            )
        else:
            return HttpResponse(
                form.errors.as_json(),
                status=400
            )
        return HttpResponse(status=200)
    return HttpResponse(status=403)

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
        else:
            return HttpResponse(
                form.errors.as_json(),
                status=400
            )
        return HttpResponse(status=200)
    return HttpResponse(status=403)

@csrf_protect
def track_delete(request):
    """ Creates a Track object. """

    if request.method == 'POST' and request.is_ajax and request.user.is_authenticated:
        pk = request.POST['pk']
        models.Track.objects.get(pk=pk).delete()
        return HttpResponse(status=200)
    return HttpResponse(status=403)

@csrf_protect
def track_sort(request):
    """ Sorts Tracks related to a specific audioset. """

    if request.method == 'POST' and request.is_ajax and request.user.is_authenticated:
        tracks = models.Track.objects.filter(audioset=request.POST['audioset'])
        for track in tracks:
            track.order = request.POST['track_' + str(track.pk)]
        bulk_update(tracks)
        return HttpResponse(status=200)
    return HttpResponse(status=403)

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
    return HttpResponse(status=403)

@csrf_protect
def clip_create(request):
    """ Creates a Clip object. """

    if request.method == 'POST' and request.is_ajax and request.user.is_authenticated:
        data = request.POST
        form = forms.ClipFormAjax(data)
        if form.is_valid():
            track = models.Track.objects.get(pk=data['track'])
            new_clip = form.save()
            track.clips.add(new_clip)
            track.save()
        else:
            return HttpResponse(
                clipform.errors.as_ul(),
                content_type="text/html",
                status=400
            )
        return HttpResponse(status=200)
    return HttpResponse(status=403)

@csrf_protect
def clip_update(request):
    """ Creates a Clip object. """

    if request.method == 'POST' and request.is_ajax and request.user.is_authenticated:
        data = request.POST
        clip = models.Clip.objects.get(pk=data['pk'])
        clipform = forms.ClipUpdateFormAjax(data, files=request.FILES, instance=clip)
        if clipform.is_valid():
            if 'image_delete' in data:
                clip.image = None
            clipform.save()
        else:
            return HttpResponse(
                clipform.errors.as_json(),
                status=400
            )
        return HttpResponse(status=200)
    return HttpResponse(status=403)

@csrf_protect
def clip_delete(request):
    """ Creates a Clip object. """

    if request.method == 'POST' and request.is_ajax and request.user.is_authenticated:
        pk = request.POST['pk']
        models.Clip.objects.get(pk=pk).delete()
        return HttpResponse(status=200)
    return HttpResponse(status=403)

@csrf_protect
def clip_sort(request):
    """ Sorts Clips related to a specific track. """

    if request.method == 'POST' and request.is_ajax and request.user.is_authenticated:
        clips = models.Clip.objects.filter(track=request.POST['track'])
        for clip in clips:
            clip.order = request.POST['clip_' + str(clip.pk)]
        bulk_update(clips)
        return HttpResponse(status=200)
    return HttpResponse(status=403)
