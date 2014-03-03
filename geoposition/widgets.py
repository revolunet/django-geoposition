from __future__ import unicode_literals

from django import forms
from django.template.loader import render_to_string
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from .conf import settings


class GeopositionWidget(forms.MultiWidget):
    def __init__(self, zoom=False, attrs=None):
        widgets = [
            forms.TextInput(),
            forms.TextInput()
        ]
        self.zoom = zoom
        if zoom:
            widgets.append(forms.TextInput())

        super(GeopositionWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, six.text_type):
            return value.rsplit(',')
        if value:
            return [value.latitude, value.longitude, value.zoom]
        return [None,None]

    def format_output(self, rendered_widgets):
        template_data = {
            'latitude': {
                'html': rendered_widgets[0],
                'label': _("latitude"),
            },
            'longitude': {
                'html': rendered_widgets[1],
                'label': _("longitude"),
            },
            'config': {
                'map_widget_height': settings.GEOPOSITION_MAP_WIDGET_HEIGHT
            }
        }
        if self.zoom :
            template_data['zoom'] = {
                'html': rendered_widgets[2],
                'label': _("zoom")
            }
        return render_to_string('geoposition/widgets/geoposition.html', template_data)

    class Media:
        js = (
            '//maps.google.com/maps/api/js?sensor=false',
            'geoposition/geoposition.js',
        )
        css = {
            'all': ('geoposition/geoposition.css',)
        }
