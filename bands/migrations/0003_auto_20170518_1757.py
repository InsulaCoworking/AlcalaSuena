# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-18 15:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0002_auto_20170518_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='band',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='band',
            name='embed_code',
            field=models.TextField(blank=True, null=True),
        ),
    ]
