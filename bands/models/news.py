from __future__ import unicode_literals

from django.db import models

from bands.helpers import RandomFileName


class News(models.Model):
    title = models.CharField(null=False, max_length=300)
    text = models.TextField(null=True, blank=True)
    image  = models.ImageField(null=True, blank=True, upload_to=RandomFileName('news/'), verbose_name='Imagen de noticia')
    btn_text  = models.CharField(null=True, blank=True, max_length=200)
    btn_link = models.CharField(null=True, blank=True, max_length=200)
    native_code  = models.IntegerField(null=True, blank=True)

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    caducity = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Noticia'
        verbose_name_plural = 'Noticias'
        ordering = ['start_date', 'end_date']

    def __unicode__(self):
        return self.title