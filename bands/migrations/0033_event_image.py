# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2021-05-21 12:11
from __future__ import unicode_literals

import bands.helpers
from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0032_auto_20210514_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=bands.helpers.RandomFileName(b'event/'), verbose_name=b'Imagen del evento'),
        ),
    ]
