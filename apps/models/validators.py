# python
import datetime
# django
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

# validators

def album_year_validator(value):
    if value < 1900 or value > datetime.datetime.now().year:
        raise ValidationError(
            _('Estás seguro de que %(value)s es el año de lanzamiento? '),
            params={'value': value}
        )
