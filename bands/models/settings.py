# coding=utf-8
from django.db import models

from bands.models import Band, Venue


class Settings(models.Model):
    key = models.CharField(null=False, blank=False, verbose_name='identificador', primary_key=True, max_length=240)
    value = models.CharField(null=True, blank=True, verbose_name='valor', max_length=240)

    class Meta:
        verbose_name = 'Configuraciones'
        verbose_name_plural = 'Configuración'
        ordering = ['key']

    def __unicode__(self):
        return self.key