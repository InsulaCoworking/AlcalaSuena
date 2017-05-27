from __future__ import unicode_literals

from django.db import models

class Tag(models.Model):
    name = models.CharField(null=False, verbose_name='Etiqueta', max_length=240)
    id = models.CharField(null=False, primary_key=True, max_length=20)
    description = models.TextField(null=True, blank=True)
    color = models.CharField(null=False, default='#FFFFFFFF', max_length=10)

    class Meta:
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Etiquetas'
        ordering = ['name']

    def __unicode__(self):
        return self.name