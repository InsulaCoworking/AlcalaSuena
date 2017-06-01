import os
import uuid

import datetime
from django.utils.deconstruct import deconstructible

# Random name generator to avoid file overwrites
@deconstructible
class RandomFileName(object):
    def __init__(self, path):
        self.path = os.path.join(path, "%s%s")

    def __call__(self, _, filename):
        # @note It's up to the validators to check if it's the correct file type in name or if one even exist.
        extension = os.path.splitext(filename)[1]
        return self.path % (uuid.uuid4(), extension)

LATENIGHT_HOURS = datetime.time(5, 0, 0)
def order_latenight(event_a, event_b):
    if event_a.time == event_b.time:
        return 0
    elif event_a.time < LATENIGHT_HOURS:
        if event_b.time < LATENIGHT_HOURS:
            return -1 if event_a.time < event_b.time else 1
        else:
            return -1
    elif event_b.time < LATENIGHT_HOURS:

        return -1
    else:
        return -1 if event_a.time < event_b.time else 1