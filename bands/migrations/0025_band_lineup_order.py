# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-04-27 14:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0024_band_newfields'),
    ]

    operations = [
        migrations.AddField(
            model_name='band',
            name='lineup_order',
            field=models.IntegerField(default=3, verbose_name='L\xednea de cartel (1, 2 o 3)'),
        ),
    ]
