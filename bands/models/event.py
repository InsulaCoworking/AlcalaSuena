import math
from django.db import models
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit

from bands.helpers import LATENIGHT_HOURS, RandomFileName
from bands.mixins import UpdateDataVersionMixin
from bands.models import Band, Venue


class Event(UpdateDataVersionMixin, models.Model):
    venue = models.ForeignKey(Venue, related_name="venue")
    bands = models.ManyToManyField(Band, related_name="band_events")
    day = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True, default=60)
    tickets_url = models.TextField(null=True, blank=True, verbose_name="Enlace entradas")
    image =  ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('event/'),
                                        processors=[ResizeToFit(512, 512, upscale=False)], format='JPEG',
                                        verbose_name='Imagen del evento')

    class Meta:
        verbose_name = 'Concierto'
        verbose_name_plural = 'Conciertos'
        ordering = ['day', 'time']


    def __unicode__(self):
        if (self.bands.all()):
            return ' + '.join([bandname for bandname in self.bands.values_list('name', flat=True)])
        return str(self.day)
