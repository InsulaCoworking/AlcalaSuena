# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2019-02-27 17:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0008_contestband_instagram_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestband',
            name='is_validated',
            field=models.BooleanField(default=False, verbose_name='Criterios validados'),
        ),
    ]
