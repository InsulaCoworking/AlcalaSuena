# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit

from bands.helpers import RandomFileName


class ArchivedYear(models.Model):
    archive_year = models.IntegerField(verbose_name='Año', null=False, blank=False, unique=True)
    main_logo = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('archive/'),
                                        processors=[ResizeToFit(1200, 400, upscale=False)], format='JPEG',
                                        verbose_name='Imagen cabecera')
    bg_image = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('archive/'),
                                    processors=[ResizeToFit(1200, 400, upscale=False)], format='JPEG',
                                    verbose_name='Imagen de fondo')

    main_color = models.CharField(null=False, default='#FFFFFFFF', max_length=10, verbose_name='Color principal')
    front_color = models.CharField(null=False, default='#000000', max_length=10, verbose_name='Color texto principal')

    class Meta:
        verbose_name = 'Archivo'
        verbose_name_plural = 'Años archivados'
        ordering = ['archive_year']

    def __unicode__(self):
        return str(self.archive_year)

