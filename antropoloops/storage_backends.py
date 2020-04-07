# django
from django.conf import settings
# contrib
from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    location = settings.S3_MEDIA_FOLDER
    file_overwrite = False
