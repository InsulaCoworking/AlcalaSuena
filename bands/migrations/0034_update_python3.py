# Generated by Django 3.2.16 on 2023-02-07 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0033_event_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='tickets_url',
            field=models.TextField(blank=True, null=True, verbose_name='Enlace entradas'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='key',
            field=models.CharField(max_length=240, primary_key=True, serialize=False, verbose_name='identificador'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='value',
            field=models.CharField(blank=True, max_length=240, null=True, verbose_name='valor'),
        ),
    ]