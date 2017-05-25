# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from bands.helpers import RandomFileName
from bands.models import Tag


class Band(models.Model):
    name = models.CharField(null=False, verbose_name='Nombre', max_length=240)
    tag = models.ForeignKey(Tag, related_name="band")
    genre = models.CharField(null=True, blank=True, verbose_name='etiqueta', max_length=240)
    profile_image = models.ImageField(null=True, blank=True, upload_to=RandomFileName('band/'))
    band_image = models.ImageField(null=True, blank=True, upload_to=RandomFileName('band/'))
    city = models.CharField(null=True, blank=True, verbose_name='Ciudad', max_length=140)
    num_members = models.IntegerField(null=True, blank=True, default=1)
    description = models.TextField(null=True, blank=True)
    embed_code = models.TextField(null=True, blank=True)

    facebook_link = models.CharField(null=True, blank=True, verbose_name='Página de Facebook', max_length=250)
    youtube_link = models.CharField(null=True, blank=True, verbose_name='Canal de Youtube', max_length=250)
    twitter_link = models.CharField(null=True, blank=True, verbose_name='Perfil de Twitter', max_length=250)
    bandcamp_link = models.CharField(null=True, blank=True, verbose_name='Página de BandCamp', max_length=250)
    presskit_link = models.CharField(null=True, blank=True, verbose_name='Presskit', max_length=250)

    class Meta:
        verbose_name = 'Banda'
        verbose_name_plural = 'Bandas'
        ordering = ['name']

    def __unicode__(self):
        return self.name


class BandToken(models.Model):
    token = models.CharField(null=False, verbose_name='Nombre', max_length=40, unique=True)
    band = models.ForeignKey(Band)
    expiration_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'
        ordering = ['band']

    def __unicode__(self):
        return self.band.name + ':' + self.token
