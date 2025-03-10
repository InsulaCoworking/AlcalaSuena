# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-18 15:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='band',
            old_name='youtube_embed',
            new_name='embed_code',
        ),
        migrations.AlterField(
            model_name='band',
            name='city',
            field=models.CharField(max_length=140, verbose_name='Ciudad'),
        ),
        migrations.AlterField(
            model_name='band',
            name='genre',
            field=models.CharField(max_length=240, verbose_name='etiqueta'),
        ),
        migrations.AlterField(
            model_name='band',
            name='tag',
            field=models.CharField(max_length=140, verbose_name='etiqueta'),
        ),
    ]
