# python
import json
import time
# django
from django.core import serializers
from django.utils.text import slugify
# project
from apps.models import models

class PropBaseSerializer(serializers.base.Serializer):
    """
    Custom serializer class which enables us to specify a subset
    of model class properties (as well as fields)
    @see https://bonidjukic.github.io/2019/02/04/serialize-django-model-class-properties.html
    """
    def serialize(self, queryset, **options):
        self.selected_props = options.pop('props')
        return super().serialize(queryset, **options)

    def serialize_property(self, obj):
        model = type(obj)
        for prop in self.selected_props:
            if hasattr(model, prop) and type(getattr(model, prop)) == property:
                self.handle_prop(obj, prop)

    def handle_prop(self, obj, prop):
        self._current[prop] = getattr(obj, prop)

    def end_object(self, obj):
        self.serialize_property(obj)
        super().end_object(obj)


class PropPythonSerializer(PropBaseSerializer, serializers.python.Serializer):
    pass


class PropJsonSerializer(PropPythonSerializer, serializers.json.Serializer):
    pass


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
            'id'             : audioset.id,
            'title'          : audioset.name,
            'publish_path'   : audioset.slug,
            'description'    : audioset.description,
            'logo_url'       : audioset.image.url if audioset.image else '',
            'background_url' : audioset.background.url if audioset.image else '',
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
            'parent_path' : '',
            'description' : audioset.description,
            'readme'      : audioset.readme,
            'logo_url'    : audioset.image.url if audioset.image else '',
        },
        # audio
        'audio' : {
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
    if audioset.mode_display is 1:
        audioset_data['visuals']['mode'] = 'map'
        audioset_data['visuals']['geomap'] = {
            'url' : '',
            'scaleFactor' : '',
            'center' : {
                'x' : 0,
                'y' : 0,
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

    for track in tracks:
        track_data = {
            'id'       : '', # TODO: review if ID is important
            'name'     : track.name,
            'color'    : track.color,
            'volume'   : None,
            'position' : track.order,
            'clipIds'  : []
        }
        for clip in track.clips.all():
            track_data['clipIds'].append( slugify(clip.name) )
            audioset_data['clips'].append({
                'id'       : slugify(clip.name),
                'name'     : clip.name,
                'trackId'  : "",
                'trackNum' : 0,
                'position' : [
                    clip.pos_x,
                    clip.pos_y
                ],
                'title'     : clip.name,
                'album'     : clip.album_name,
                'artist'    : clip.artist,
                'country'   : clip.country.code,
                'place'     : clip.place,
                'year'      : clip.year,
                'readme'    : clip.readme,
                'key'       : clip.key,
                'beats'     : 16,
                'volume'    : None,
                'keyMap'    : clip.key,
                'color'     : '',
                'coverUrl'  : clip.image.url if clip.image else None,
                'audioUrl'  : '',
                'resources' : '',
                'audio'     : {
                    'beats'  : 16,
                    'volume' : None,
                },
            })

        audioset_data['tracks'].append(track_data)

    return json.dumps(
        audioset_data,
        indent=4,
    )
