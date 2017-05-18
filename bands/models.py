# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Band(models.Model):
    name = models.CharField(null=False, verbose_name='Nombre', max_length=240)
    tag = models.CharField(null=False, verbose_name='etiqueta', max_length=140)
    genre = models.CharField(null=False, verbose_name='etiqueta', max_length=240)
    profile_image = models.ImageField(null=True, blank=True)
    band_image = models.ImageField(null=True, blank=True)
    city = models.CharField(null=False, verbose_name='Ciudad', max_length=140)
    num_members = models.IntegerField(default=1)
    description = models.TextField(null=True, blank=True)
    embed_code = models.TextField(null=True, blank=True)
    # TODO: RSS links

    class Meta:
        verbose_name = 'Banda'
        verbose_name_plural = 'Bandas'
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Venue(models.Model):
    name = models.CharField(null=False, verbose_name='Nombre', max_length=240)
    description = models.TextField(null=False, blank=True)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    image = models.ImageField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Escenario'
        verbose_name_plural = 'Escenarios'
        ordering = ['name']

    def __unicode__(self):
        return self.name

class Event(models.Model):
    band = models.ForeignKey(Band, related_name="band")
    venue = models.ForeignKey(Venue, related_name="venue")
    day = models.DateField(null=False)
    time = models.TimeField(null=False)

    class Meta:
        verbose_name = 'Concierto'
        verbose_name_plural = 'Conciertos'
        ordering = ['day', 'time']

    def __unicode__(self):
        return self.band.name + ' - ' + str(self.day)
