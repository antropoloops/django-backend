# python
import urllib.request
import json

def load_json(resource_path):
    """ Loads a JSON object from a given resource path """

    print('Loading resource at %s' % resource_path)
    try:
        resource = urllib.request.urlopen( resource_path )
        return json.loads(
            resource.read().decode(
                resource.info().get_param('charset') or 'utf-8'
            )
        )
    except Exception as e:
        print('There\'s been a problem trying to download the resource provided')
        print( str(e) )
