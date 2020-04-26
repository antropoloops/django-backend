# python
from urllib.request import urlopen
from io import BytesIO
from django.core.files import File


def set_file_from_remote(field, url):
    """ Gets remote file from a given url """

    print('Loading asset from %s' % url)
    try:
        file = urlopen(url)
        file_bytes = BytesIO( file.read() )
        filename = url.split('/')[-1]
        field.save(
            filename,
            File( file_bytes ),
            save=True
        )
    except Exception as e:
        print(
            'There\'s been a problem trying to download the resource provided at %s. Operation cancelled.' % url
        )
        print( str(e) )
