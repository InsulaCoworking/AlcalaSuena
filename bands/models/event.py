import math
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit

from bands.helpers import LATENIGHT_HOURS, RandomFileName
from bands.mixins import UpdateDataVersionMixin
from bands.models import Band, Venue


class Event(UpdateDataVersionMixin, models.Model):
    venue = models.ForeignKey(Venue, related_name="venue", on_delete=models.CASCADE)
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

    @property
    def has_image(self):
        return self.image or (self.bands.count() == 1 and self.bands.first().profile_image)

    @property
    def profile_image(self):
        if self.image:
            return self.image
        else:
            for band in self.bands.all():
                if band.profile_image:
                    return band.profile_image

    @property
    def slug(self):
        return slugify(str(self))

    @property
    def get_detail_url(self):
        if self.bands.count() == 1:
            return reverse('band_detail', kwargs={'pk': self.bands.first().pk})
        else:
            return reverse('event_detail_slug', kwargs={'pk': self.pk, 'slug': self.slug })

    @property
    def get_band_detail_url(self):
        if self.bands.count() == 1:
            return reverse('venue_detail', kwargs={'pk':self.venue.pk })
        else:
            return self.get_detail_url

    def __str__(self):
        if (self.bands.all()):
            return ' + '.join([bandname for bandname in self.bands.values_list('name', flat=True)])
        return str(self.day)

    def __unicode__(self):
        if (self.bands.all()):
            return ' + '.join([bandname for bandname in self.bands.values_list('name', flat=True)])
        return str(self.day)
