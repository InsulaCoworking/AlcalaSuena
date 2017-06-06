# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from bands.helpers import RandomFileName
from bands.models import Tag, Band, Venue


class BillingInfo(models.Model):
    band = models.ForeignKey(Band, verbose_name='Banda')
    cif = models.CharField(null=True, blank=True, verbose_name='NIF/CIF', max_length=250)
    uploaded = models.DateTimeField(auto_now_add=True)
    contact_name = models.CharField(null=True, blank=True, verbose_name='Persona de contacto', max_length=250)
    contact_email = models.CharField(null=True, blank=True, verbose_name='Email de contacto', max_length=250)
    contact_phone = models.CharField(null=True, blank=True, verbose_name='Teléfono de contacto', max_length=250)
    venue = models.ForeignKey(Venue, verbose_name='Escenario en el que tocaron')
    num_members = models.IntegerField(null=True, blank=True, default=1, verbose_name='Número de componentes')
    billing_total = models.FloatField(null=True, blank=True, verbose_name='Importe TOTAL Factura')
    billing_file = models.FileField(upload_to=RandomFileName('bills/'), verbose_name='Factura')

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['uploaded']
