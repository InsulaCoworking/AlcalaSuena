import math
from django.db import models

from bands.helpers import LATENIGHT_HOURS
from bands.mixins import UpdateDataVersionMixin
from bands.models import Band, Venue


class Event(UpdateDataVersionMixin, models.Model):
    venue = models.ForeignKey(Venue, related_name="venue")
    bands = models.ManyToManyField(Band, related_name="band_events")
    day = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True, default=60)
    tickets_url = models.TextField(null=True, blank=True, verbose_name="Enlace entradas")

    class Meta:
        verbose_name = 'Concierto'
        verbose_name_plural = 'Conciertos'
        ordering = ['day', 'time']


    def __unicode__(self):
        if (self.bands.all()):
            return ' + '.join([str(bandname) for bandname in self.bands.values_list('name', flat=True)])
        return str(self.day)
