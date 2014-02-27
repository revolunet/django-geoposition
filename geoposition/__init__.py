from __future__ import unicode_literals

from decimal import Decimal

VERSION = (0, 2, 0, 'pre')
__version__ = '.'.join(map(str, VERSION))


class Geoposition(object):
    def __init__(self, latitude, longitude, zoom=0):
        if isinstance(latitude, float) or isinstance(latitude, int):
            latitude = str(latitude)
        if isinstance(longitude, float) or isinstance(longitude, int):
            longitude = str(longitude)
        if isinstance(zoom, float) or isinstance(zoom, int):
            zoom = str(zoom)
        self.latitude = Decimal(latitude)
        self.longitude = Decimal(longitude)
        self.zoom = zoom

    def __str__(self):
        return "%s,%s,%s" % (self.latitude, self.longitude, self.zoom)

    def __repr__(self):
        return "Geoposition(%s)" % str(self)

    def __len__(self):
        return len(str(self))

    def __eq__(self, other):
        return isinstance(other, Geoposition) and self.latitude == other.latitude and self.longitude == other.longitude

    def __ne__(self, other):
        return not isinstance(other, Geoposition) or self.latitude != other.latitude or self.longitude != other.longitude
