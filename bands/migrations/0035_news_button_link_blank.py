# Generated by Django 3.2.16 on 2023-05-10 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0034_update_python3'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='btn_link',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='Link del botón'),
        ),
        migrations.AlterField(
            model_name='news',
            name='btn_text',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='Texto del botón'),
        ),
    ]
