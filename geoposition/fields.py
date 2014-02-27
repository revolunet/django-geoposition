from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_text

from . import Geoposition
from .forms import GeopositionField as GeopositionFormField


class GeopositionField(models.Field):
    description = _("A geoposition (latitude and longitude)")
    __metaclass__ = models.SubfieldBase

    def __init__(self, zoom=False, *args, **kwargs):
        kwargs['max_length'] = 45
        self.zoom = zoom
        super(GeopositionField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'CharField'

    def to_python(self, value):
        if not value or value == 'None':
            return None
        if isinstance(value, Geoposition):
            return value
        if isinstance(value, list):
            return Geoposition(*value)

        # default case is string
        value_parts = value.rsplit(',')
        try:
            latitude = value_parts[0]
        except IndexError:
            latitude = '0.0'
        try:
            longitude = value_parts[1]
        except IndexError:
            longitude = '0.0'
        try:
            zoom = value_parts[2]
        except IndexError:
            zoom = '0'

        return Geoposition(latitude, longitude, zoom)

    def get_prep_value(self, value):
        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return smart_text(value)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': GeopositionFormField,
            'zoom': self.zoom
        }
        defaults.update(kwargs)
        return super(GeopositionField, self).formfield(**defaults)
