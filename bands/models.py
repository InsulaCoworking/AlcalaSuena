# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Band(models.Model):
    name = models.CharField(null=False, verbose_name='Nombre', max_length=240)
    tag = models.CharField(null=False, verbose_name='etiqueta', max_length=140)
    genre = models.CharField(null=False, verbose_name='etiqueta', max_length=240)
    profile_image = models.ImageField(null=True)
    band_image = models.ImageField(null=True)
    city = models.CharField(null=False, verbose_name='Ciudad', max_length=140)
    num_members = models.IntegerField(default=1)
    description = models.TextField(null=True)
    embed_code = models.TextField(null=True)
    # TODO: RSS links

    class Meta:
        verbose_name = 'Banda'
        verbose_name_plural = 'Bandas'
        ordering = ['name']

    def __unicode__(self):
        return self.name
