from django.apps import AppConfig


class ModelsConfig(AppConfig):
    name = 'apps.models'

    def ready(self):
        from . import signals
