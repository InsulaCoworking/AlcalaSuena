# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

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