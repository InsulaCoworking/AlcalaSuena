import itertools

from datetime import datetime, time
from django import template

from bands.helpers import LATENIGHT_HOURS
from bands.models import Event

register = template.Library()

@register.filter
def chunks(value, chunk_length):
    """
    Breaks a list up into a list of lists of size <chunk_length>
    """
    clen = int(chunk_length)
    i = iter(value)
    while True:
        chunk = list(itertools.islice(i, clen))
        if chunk:
            yield chunk
        else:
            break


@register.filter
def js_date(value, default=0):
    """
    Returns code to create a JS Date
    """
    if isinstance(value, Event):
        return 'new Date(Date.UTC({},{},{},{},{}))'.format(value.day.year, value.day.month - 1,
                                                           value.day.day + (1 if value.time < LATENIGHT_HOURS else 0),
                                                           value.time.hour, value.time.minute)
    else:
        date = datetime.combine(value, time(default, 0, 0 ))
        return 'new Date(Date.UTC({},{},{},{},{}))'.format(date.year, date.month - 1,
                                                           date.day ,date.hour, date.minute)