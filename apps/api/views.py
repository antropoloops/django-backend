# python
import json
# django
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.core import serializers
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.cache import cache
from django.http import HttpRequest
from django.utils.cache import get_cache_key
from django.views.decorators.cache import cache_page
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
@login_required
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
@login_required
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
@login_required
def track_delete(request):
    """ Creates a Track object. """

    data = request.POST
    if request.method == 'POST' and request.is_ajax and request.user.is_authenticated:
        models.Track.objects.get(pk=data['pk']).delete()
        return HttpResponse(status=200)
    return HttpResponse(status=403)


@csrf_protect
@login_required
def track_sort(request):
    """ Sorts Tracks related to a specific audioset. """

    if request.method == 'POST' and request.is_ajax and request.user.is_authenticated:
        tracks = models.Track.objects.filter(audioset=request.POST['audioset'])
        for track in tracks:
            track.order = request.POST['track_' + str(track.pk)]
        bulk_update(tracks)
        return HttpResponse(status=200)
    return HttpResponse(status=403)

@login_required
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
@login_required
def clip_create(request):
    """ Creates a Clip object. """

    if request.method == 'POST' and request.is_ajax and request.user.is_authenticated:
        data = request.POST
        form = forms.ClipForm(data, files=request.FILES)
        if form.is_valid():
            track = models.Track.objects.get(pk=data['track'])
            new_clip = form.save()
            track.clips.add(new_clip)
            track.save()
        else:
            return HttpResponse(
                form.errors.as_json(),
                content_type="application/json",
                status=400
            )
        return HttpResponse(status=200)
    return HttpResponse(status=403)


@csrf_protect
@login_required
def clip_update(request):
    """ Updates a Clip object. """

    if request.method == 'POST' and request.is_ajax and request.user.is_authenticated:
        data = request.POST
        clip = models.Clip.objects.get(pk=data['pk'])
        clipform = forms.ClipUpdateForm(
            data,
            files=request.FILES,
            instance=clip
        )
        if clipform.is_valid():
            for field in [
                'image',
                'audio_wav',
            ]:
                if '%s_delete'%field in data:
                    setattr(clip, field, None)
            clipform.save()
        else:
            return HttpResponse(
                clipform.errors.as_json(),
                content_type="application/json",
                status=400
            )
        return HttpResponse(status=200)
    return HttpResponse(status=403)


@csrf_protect
@login_required
def clip_delete(request):
    """ Creates a Clip object. """
    data = request.POST
    if request.method == 'POST' and request.is_ajax and request.user.is_authenticated:
        models.Clip.objects.get(pk=data['pk']).delete()
        return HttpResponse(status=200)
    return HttpResponse(status=403)


@csrf_protect
@login_required
def clip_sort(request):
    """ Sorts Clips related to a specific track. """

    if request.method == 'POST' and request.is_ajax and request.user.is_authenticated:
        clips = models.Clip.objects.filter(track=request.POST['track'])
        for clip in clips:
            clip.order = request.POST['clip_' + str(clip.pk)]
        bulk_update(clips)
        return HttpResponse(status=200)
    return HttpResponse(status=403)


def audioset(request, slug):
    """ Gets an audioset object """

    audioset = get_object_or_404(
        models.Audioset.objects,
        slug=slug
    )

    return HttpResponse(
        serializers.serialize_audioset(audioset),
        content_type="application/json",
        status=200
    )

def projects(request):
    """ Gets projects """

    projects = models.Project.objects.filter(published=True)

    return HttpResponse(
        serializers.serialize_project(projects),
        content_type="application/json",
        status=200
    )


def project(request, slug):
    """ Gets an project object """

    project = get_object_or_404(
        models.Project.objects,
        slug=slug
    )

    return HttpResponse(
        serializers.serialize_project(project),
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


def theme(request, slug):
    """ Gets Theme by slug """

    theme = get_object_or_404(
        models.Theme.objects,
        slug=slug
    )

    return HttpResponse(
        serializers.serialize_theme(theme),
        content_type="application/json",
        status=200
    )

def home(request):
    """ Gets Home """
    theme = get_object_or_404(
        models.Theme.objects,
        slug='home'
    )
    return HttpResponse(
        serializers.serialize_home(theme),
        content_type="application/json",
        status=200
    )

# @cache_page(60 * 60 * 24)
def resource(request, slug):
    """ Gets a resource """

    try:
        resource = models.Audioset.objects.get(slug=slug)
        data = serializers.serialize_audioset(resource),
    except models.Audioset.DoesNotExist:
        try:
            resource = models.Project.objects.get(slug=slug)
            data = serializers.serialize_project(resource)
        except models.Project.DoesNotExist:
            return HttpResponse(
                status=404
            )
    return HttpResponse(
        data,
        content_type="application/json",
        status=200
    )

@login_required
def clean_cache(request, slug):
    request = HttpRequest()
    path = reverse(
        'resource',
        kwargs = { 'slug' : slug }
    )
    request.path = path
    key = get_cache_key(slug)
    if cache.has_key(key):
        cache.delete(key)
    return HttpResponse(
        data,
        content_type="application/json",
        status=200
    )

@login_required
def audioset_toggle(request, pk):
    audioset = get_object_or_404(
        models.Audioset.objects,
        pk=pk
    )
    audioset.published = not audioset.published
    audioset.save()
    return HttpResponse(
        {},
        content_type="application/json",
        status=200
    )
