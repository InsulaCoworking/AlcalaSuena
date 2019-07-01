# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, Avg
from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import ResizeToFit, ResizeToFill
from bands.helpers import RandomFileName
from bands.models import Tag



class ArchivedYear(models.Model):
    archive_year = models.IntegerField(verbose_name='Año', null=True, blank=True)
    main_logo = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('contest/'),
                                        processors=[ResizeToFit(512, 512, upscale=False)], format='JPEG',
                                        verbose_name='Imagen principal')


    class Meta:
        verbose_name = 'Miembro de banda'
        verbose_name_plural = 'Miembros de bandas'
        ordering = ['band']

    def __unicode__(self):
        return self.band.name + ': ' + self.full_name

