# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2019-02-25 11:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0026_band_secondary_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='btn_link',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Link del bot\xf3n'),
        ),
        migrations.AlterField(
            model_name='news',
            name='btn_text',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Texto del bot\xf3n'),
        ),
        migrations.AlterField(
            model_name='news',
            name='caducity',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Caducidad'),
        ),
        migrations.AlterField(
            model_name='news',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fecha de fin'),
        ),
        migrations.AlterField(
            model_name='news',
            name='native_code',
            field=models.IntegerField(blank=True, null=True, verbose_name='C\xf3digo nativo'),
        ),
        migrations.AlterField(
            model_name='news',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fecha de inicio'),
        ),
        migrations.AlterField(
            model_name='news',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='Texto'),
        ),
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(max_length=300, verbose_name='T\xedtulo'),
        ),
    ]
