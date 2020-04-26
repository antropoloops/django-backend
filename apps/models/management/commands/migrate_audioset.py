# django
from django.utils.text import slugify
# project
from apps.models import models
from django.conf import settings
from .load_json import load_json
from .set_file_from_remote import set_file_from_remote


def migrate_audioset(audioset_data, project):
    """ Migrates an Audioset from a json data representation """

    audioset_meta    = audioset_data['meta']
    audioset_audio   = audioset_data['audio']
    audioset_visuals = audioset_data['visuals']
    audioset_mode    = audioset_visuals['mode']
    audioset_tracks  = audioset_data['tracks']
    is_map           = audioset_mode == 'map'
    audioset = models.Audioset(
        name = audioset_meta['title'],
        slug = slugify( audioset_meta['title'] ),
        description = audioset_meta['description'],
        readme = audioset_meta['readme'],
        # project
        project = project,
        # audio
        audio_bpm = audioset_audio['bpm'],
        audio_quantize = audioset_audio['quantize'],
        # visuals
        mode_display = '2' if is_map else '1',
        # map
        map_url = audioset_visuals['geomap']['url'] if is_map else None,
        map_scale = audioset_visuals['geomap']['scaleFactor'] if is_map else 1,
        map_center_x = audioset_visuals['geomap']['center']['x'] if is_map else 0,
        map_center_y = audioset_visuals['geomap']['center']['y'] if is_map else 0,
    )
    # Assets
    # image
    set_file_from_remote( audioset.image, audioset_meta['logo_url'] )
    # panel background
    if not is_map:
        background = audioset_visuals['image']['url']
        set_file_from_remote( audioset.background, background )

    audioset.save()

    # CLIPS
    clips = {}
    for clip_data in audioset_data['clips']:
        print('Loading clip "%s"' % clip_data['name'])
        clip = models.Clip(
            name = clip_data['name'],
            audio_name = clip_data['title'],
            album_name = clip_data['album'],
            artist = clip_data['artist'],
            country = clip_data['country'],
            place = clip_data['place'],
            year = int(clip_data['year']) if clip_data['year'] else None,
            key = clip_data['key'],
            beats = clip_data['audio']['beats'],
            volume = clip_data['audio']['volume'],
            pos_x = clip_data['position'][0],
            pos_y = clip_data['position'][1]
        )
        # Assets
        set_file_from_remote( clip.image, clip_data['coverUrl'] )
        audio = ['mp3', 'wav', 'ogg']
        for format in audio:
            if format in clip_data['resources']['audio']:
                set_file_from_remote(
                    clip.audio_mp3,
                    clip_data['resources']['audio'][format]
                )
        clip.save()

        # Store in tracks lut
        track = clip_data['trackId']
        if track in clips:
            clips[track].append( clip )
        else:
            clips[track] = [ clip ]

    # TRACKS
    for track_data in audioset_tracks:
        print('Loading track "%s"' % track_data['name'])
        track = models.Track(
            name = track_data['name'],
            order = track_data['position'],
            color = track_data['color'],
            volume = track_data['volume'],
            audioset = audioset
        )
        track.save()
        print('Assigning clips to track "%s"' % track_data['name'])
        track.clips.set( clips[ track_data['id'] ] )
