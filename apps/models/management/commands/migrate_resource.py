
# django
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
# project
from apps.models import models
from django.conf import settings
from .load_json import load_json
from .set_file_from_remote import set_file_from_remote
from .migrate_audioset import migrate_audioset

"""
A manage.py command to migrate a project given a path that exposes it in JSON
following the structure given in apps
"""

class Command(BaseCommand):

    """
    Adds the path to project resource
    """
    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            help='Provide a path to audioset',
        )

    """
    Imports Audioset
    """
    def handle(self, *args, **options):
        path = get_path(options['path'])
        resource_data = load_json( path )
        resource_meta  = resource_data['meta']

        # Create project
        print('Creating project %s' % resource_meta['title'])
        project = models.Project(
            name = resource_meta['title'],
            slug = slugify(resource_meta['title']),
            description = resource_meta['description'],
            readme = resource_meta['readme'],
        )
        # image
        set_file_from_remote(
            project.image,
            resource_meta['logo_url']
        )
        project.save()
        # Create audiosets
        if 'audiosets' in resource_data:
            for audioset in resource_data['audiosets']:
                path = get_path(audioset['publish_path'])
                audioset_data = load_json(path)
                migrate_audioset(audioset_data, project)
        else:
            migrate_audioset(resource_data, project)

def get_path(subpath):
    return '%s/%s.%s' % (
        settings.MIGRATION_ENDPOINT,
        subpath,
        settings.MIGRATION_ENDPOINT_SUFFIX
    )
