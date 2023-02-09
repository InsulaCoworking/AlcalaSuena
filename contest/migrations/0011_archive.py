# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2019-07-02 16:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0010_contestband_validated_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestband',
            name='archive_year',
            field=models.IntegerField(blank=True, null=True, verbose_name='A\xf1o'),
        ),
        migrations.AddField(
            model_name='contestband',
            name='archived',
            field=models.BooleanField(default=False, verbose_name='Archivada'),
        ),
    ]
