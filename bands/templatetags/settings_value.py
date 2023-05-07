from django import template
from django.conf import settings

register = template.Library()

ALLOWABLE_VALUES = ("GMAPS_APIKEY", "ANALYTICS_KEY", "MAIN_PAGE_TITLE", "BASESITE_URL", "INITIAL_LATITUDE",
                    "INITIAL_LONGITUDE", "GOOGLE_ANALYTICS_UA", "GOOGLE_ANALYTICS_TAG")

# settings value (based on https://stackoverflow.com/a/21593607)
@register.simple_tag
def settings_value(name):
    if name in ALLOWABLE_VALUES:
        return getattr(settings, name, '')
    return ''