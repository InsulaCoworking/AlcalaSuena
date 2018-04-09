from django import template
from django.conf import settings

register = template.Library()

ALLOWABLE_VALUES = ("GMAPS_APIKEY", "ANALYTICS_KEY", "MAIN_PAGE_TITLE", "INITIAL_LATITUDE", "INITIAL_LONGITUDE")

# settings value (based on https://stackoverflow.com/a/21593607)
@register.simple_tag
def settings_value(name):
    if name in ALLOWABLE_VALUES:
        return getattr(settings, name, '')
    return ''