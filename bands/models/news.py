# coding=utf-8
from __future__ import unicode_literals

from django.db import models

from bands.helpers import RandomFileName


class News(models.Model):
    title = models.CharField(null=False, max_length=300, verbose_name='Título')
    text = models.TextField(null=True, blank=True, verbose_name='Texto')
    image  = models.ImageField(null=True, blank=True, upload_to=RandomFileName('news/'), verbose_name='Imagen de noticia')
    btn_text  = models.CharField(null=False, blank=True, max_length=200, verbose_name='Texto del botón', default="")
    btn_link = models.CharField(null=False, blank=True, max_length=200, verbose_name='Link del botón', default="")
    native_code  = models.IntegerField(null=True, blank=True, verbose_name='Código nativo')

    start_date = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de inicio')
    end_date = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de fin')
    caducity = models.DateTimeField(null=True, blank=True, verbose_name='Caducidad')

    class Meta:
        verbose_name = 'Noticia'
        verbose_name_plural = 'Noticias'
        ordering = ['start_date', 'end_date']

    def __unicode__(self):
        return self.title