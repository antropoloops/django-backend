# python
import json
# django
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.core import serializers
from django.shortcuts import get_list_or_404, get_object_or_404
from django.conf import settings
# contrib
from bulk_update.helper import bulk_update
# app
from . import serializers
from apps.dashboard import forms
from apps.models import models


def track(request, pk):
    """ Get Track object. """

    if request.is_ajax and request.user.is_authenticated:
        track = models.Track.objects.get(pk=pk)
        data = serializers.TrackSerializer(track).data
        return JsonResponse(
            data,
            safe=False
        )
    return HttpResponse(status=403)


def track_clips(request, pk):
    """ Get Track clips. """

    if request.is_ajax and request.user.is_authenticated:
        clips = models.Clip.objects.filter(track__audioset=pk)
        data = serializers.MapClipSerializer(clips, many=True).data
        return JsonResponse(
            data,
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

    data = request.POST
    if request.method == 'POST' and request.is_ajax and request.user.is_authenticated:
        models.Track.objects.get(pk=data['pk']).delete()
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


def clip(request, pk):
    """ Get Clip object. """

    if request.is_ajax and request.user.is_authenticated:
        clip = models.Clip.objects.get(pk=pk)
        data = serializers.ClipSerializer(clip).data
        return JsonResponse(
            data,
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
        clipform = forms.ClipUpdateFormAjax(
            data,
            files=request.FILES,
            instance=clip
        )
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
    data = request.POST
    if request.method == 'POST' and request.is_ajax and request.user.is_authenticated:
        models.Clip.objects.get(pk=data['pk']).delete()
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


def audioset(request, pk):
    """ Gets an audioset object """

    audioset = get_object_or_404(
        models.Audioset.objects,
        pk=pk
    )

    return HttpResponse(
        serialize_audioset(audioset),
        content_type="application/json",
        status=200
    )

def projects(request):
    """ Gets projects """

    projects = models.Project.objects(published=True)

    return HttpResponse(
        serialize_project(project),
        content_type="application/json",
        status=200
    )


def project(request, pk):
    """ Gets an project object """

    project = get_object_or_404(
        models.Project.objects,
        pk=pk
    )

    return HttpResponse(
        serialize_project(project),
        content_type="application/json",
        status=200
    )

def themes(request):
    """ Gets Themes """

    if request.is_ajax:
        themes = models.Theme.objects.all()

        return JsonResponse(
            serializers.ThemeSerializer(
                themes,
                many=True
            ).data,
            safe=False
        )
    return HttpResponse(status=403)
