# python
import json
import time
from collections import OrderedDict
from itertools import chain
# django
from django.utils.text import slugify
# contrib
from rest_framework import serializers
# project
from apps.models import models


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Track
        fields = [
            'pk',
            'name',
            'color',
        ]

class TrackColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Track
        fields = [ 'color', ]


class ClipSerializer(serializers.ModelSerializer):

    pk = serializers.IntegerField(
        source='id'
    )
    country = serializers.ReadOnlyField(
        source='country.code'
    )

    class Meta:
        model = models.Clip
        exclude = [
            'id',
            'audio_mp3',
            'audio_ogg',
            'image_alt',
            'place',
            'beats',
            'volume'
        ]

class MapClipSerializer(serializers.ModelSerializer):

    track = TrackColorSerializer(
        many = True
    )

    class Meta:
        model = models.Clip
        fields = [
            'pk',
            'name',
            'pos_x',
            'pos_y',
            'track'
        ]

class ThemeUnitSerializer(serializers.ModelSerializer):

    content = serializers.SerializerMethodField('get_content')

    def get_content(self, obj):
        content = obj.project if obj.project else obj.set
        return {
            'name'    : content.name,
            'slug'    : content.slug,
            'summary' : content.description,
            'image'   : content.image.url if content.image else None
        }

    class Meta:
        model = models.ThemeUnit
        fields = [
            'content',
            'order'
        ]

class ThemeSerializer(serializers.ModelSerializer):

    units = ThemeUnitSerializer(
        many = True
    )

    class Meta:
        model = models.Theme
        fields = [
            'name',
            'description',
            'units'
        ]


def serialize_theme(theme):
    """ Custom serializer for audioset objects """

    theme_data = {
        'format'          : 'atpls-audioset',
        'version'         : '2.0.0',
        'id'              : theme.slug,
        'type'            : 'project',
        'last_updated_at' : time.mktime(
            theme.update_date.timetuple()
        ),
        # meta
        'meta' : {
            'title'       : theme.name,
            'path'        : theme.slug,
            'parent_path' : '',
            'description' : theme.description,
            'readme'      : theme.readme,
            'logo_url'    : theme.image.url if theme.image else '',
        },
        'audiosets' : [],
    }

    items = models.ThemeUnit.objects.filter(
        theme=theme
    )

    for item in items:
        content = item.set or item.project
        theme_data['audiosets'].append({
            'id'             : content.play_id,
            'title'          : content.name,
            'publish_path'   : content.slug,
            'description'    : content.description,
            'logo_url'       : content.image.url if content.image else '',
        })

    return json.dumps(
        theme_data,
        indent=4,
    )

def serialize_community(audiosets):
    """ Custom serializer for audioset objects """

    theme_data = {
        'format'          : 'atpls-audioset',
        'version'         : '2.0.0',
        'id'              : 'comunidad',
        'type'            : 'project',
        'last_updated_at' : time.mktime(
            theme.update_date.timetuple()
        ),
        # meta
        'meta' : {
            'title'       : 'Comunidad',
            'path'        : 'comunidad',
            'parent_path' : '',
            'description' : 'Lorem ipsum',
            'readme'      : 'Lorem ipsum',
            'logo_url'    : theme.image.url if theme.image else '',
        },
        'audiosets' : [],
    }

    items = models.Project.objects.filter(
        published=True
    )

    for content in items:
        theme_data['audiosets'].append({
            'id'             : content.play_id,
            'title'          : content.name,
            'publish_path'   : content.slug,
            'description'    : content.description,
            'logo_url'       : content.image.url if content.image else '',
        })

    return json.dumps(
        theme_data,
        indent=4,
    )

def serialize_home(theme):
    """ Custom serializer for audioset objects """

    theme_data = {
        'format'          : 'atpls-audioset',
        'version'         : '2.0.0',
        'id'              : theme.slug,
        'type'            : 'project',
        'last_updated_at' : time.mktime(
            theme.update_date.timetuple()
        ),
        # meta
        'meta' : {
            'title'       : theme.name,
            'path'        : theme.slug,
            'parent_path' : '',
            'description' : theme.description,
            'readme'      : theme.readme,
            'logo_url'    : theme.image.url if theme.image else '',
        },
        'audiosets' : [],
    }

    items = models.Project.objects.filter(
        published=True
    )

    for content in items:
        theme_data['audiosets'].append({
            'id'             : content.play_id,
            'title'          : content.name,
            'publish_path'   : content.slug,
            'description'    : content.description,
            'logo_url'       : content.image.url if content.image else '',
        })

    return json.dumps(
        theme_data,
        indent=4,
    )

def serialize_project(project):
    """ Custom serializer for audioset objects """

    project_data = {
        'format'          : 'atpls-audioset',
        'version'         : '2.0.0',
        'id'              : project.slug,
        'type'            : 'project',
        'last_updated_at' : time.mktime(project.update_date.timetuple()),
        # meta
        'meta' : {
            'title'       : project.name,
            'path'        : project.slug,
            'parent_path' : '',
            'description' : project.description,
            'readme'      : project.readme,
            'logo_url'    : project.image.url if project.image else '',
        },
        'audiosets' : [],
    }

    for audioset in project.audiosets.all():
        project_data['audiosets'].append({
            'id'             : audioset.play_id,
            'title'          : audioset.name,
            'publish_path'   : audioset.slug,
            'description'    : audioset.description,
            'logo_url'       : audioset.image.url if audioset.image else '',
            'background_url' : audioset.background.url if audioset.background else '',
        })

    return json.dumps(
        project_data,
        indent=4,
    )


def serialize_audioset(audioset):
    """ Custom serializer for audioset objects """

    tracks = models.Track.objects.filter(audioset=audioset)

    audioset_data = {
        'format'          : 'atpls-audioset',
        'version'         : '2.0.0',
        'id'              : audioset.slug,
        'type'            : 'audioset',
        'last_updated_at' : time.mktime(audioset.update_date.timetuple()),
        # meta
        'meta' : {
            'title'       : audioset.name,
            'path'        : audioset.slug,
            'parent_path' : audioset.project.slug,
            'description' : audioset.description,
            'readme'      : audioset.readme,
            'logo_url'    : audioset.image.url if audioset.image else '',
        },
        # audio
        'audio' : {
            'mode' : audioset.playmode,
            'bpm' : 120,
            'defaults' : {
                'loop' : True,
            },
            'signature'      : [4, 4],
            'trackMaxVoices' : 1,
            'quantize'       : 1,
        },
        # visuals
        'visuals' : {},
        # tracks
        'tracks' : [],
        # clips
        'clips'  : [],
    }
    if audioset.mode_display == '2':
        audioset_data['visuals']['mode'] = 'map'
        audioset_data['visuals']['geomap'] = {
            'url' : audioset.map_url,
            'scaleFactor' : audioset.map_scale,
            'center' : {
                'x' : audioset.map_center_x,
                'y' : audioset.map_center_y,
            }
        }
    else:
        audioset_data['visuals']['mode'] = 'panel'
        audioset_data['visuals']['image'] = {}
        if audioset.background:
            audioset_data['visuals']['image'] = {
                'url' : audioset.background.url,
                'size' : {
                    'width'  : audioset.background.width,
                    'height' : audioset.background.height,
                },
            }

    for index, track in enumerate(tracks):
        track_data = {
            'id'       : track.id,
            'name'     : track.name,
            'color'    : track.color,
            'volume'   : track.volume,
            'position' : track.order,
            'clipIds'  : []
        }
        for clip in track.clips.all():
            track_data['clipIds'].append( slugify(clip.name) )
            clip_data = {
                'id'       : slugify(clip.name),
                'name'     : clip.name,
                'trackId'  : track.id,
                'trackNum' : index,
                'position' : [
                    clip.pos_x,
                    clip.pos_y
                ],
                'title'     : clip.audio_name,
                'album'     : clip.album_name,
                'artist'    : clip.artist,
                'country'   : clip.country.code,
                'place'     : clip.place,
                'year'      : clip.year,
                'readme'    : clip.readme,
                'keyboard'  : clip.key,
                'beats'     : clip.beats,
                'volume'    : clip.volume,
                'keyMap'    : clip.key,
                'color'     : track.color,
                'coverUrl'  : clip.image.url if clip.image else None,
                'audioUrl'  : '',
                'resources' : {
                    'cover' : {
                        'small' : clip.image_small.url if clip.image_small else None,
                        'thumb' : clip.image_thumb.url if clip.image_thumb else None,
                    },
                    'cover2' : {
                        'small' : '',
                        'thumb' : '',
                    },

                },
                'audio'     : {
                    'beats'  : clip.beats,
                    'volume' : clip.volume,
                },
            }
            clip_audio = {
                'wav' : clip.audio_wav.url if clip.audio_wav else None
            }
            if not clip.edited:
                clip_audio['mp3'] = clip.audio_mp3.url if clip.audio_mp3 else None,
                clip_audio['ogg'] = clip.audio_ogg.url if clip.audio_ogg else None,
            clip_data['resources']['audio'] = clip_audio
            audioset_data['clips'].append(clip_data)

        audioset_data['tracks'].append(track_data)

    return json.dumps(
        audioset_data,
        indent=4,
    )
