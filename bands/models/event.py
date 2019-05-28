import math
from django.db import models

from bands.helpers import LATENIGHT_HOURS
from bands.models import Band, Venue


class Event(models.Model):
    band = models.ForeignKey(Band, related_name="events")
    venue = models.ForeignKey(Venue, related_name="venue")
    day = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True, default=60)

    class Meta:
        verbose_name = 'Concierto'
        verbose_name_plural = 'Conciertos'
        ordering = ['day', 'time']


    def __unicode__(self):
        return self.band.name + ' - ' + str(self.day)