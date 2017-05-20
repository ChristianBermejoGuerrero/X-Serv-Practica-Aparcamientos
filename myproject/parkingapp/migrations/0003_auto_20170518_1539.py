# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parkingapp', '0002_auto_20170518_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aparcamiento',
            name='accesibilidad',
            field=models.IntegerField(null=True, default=None, blank=True),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='descripcion',
            field=models.TextField(null=True, default=None, blank=True),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='latitud',
            field=models.FloatField(null=True, default=None, blank=True),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='longitud',
            field=models.FloatField(null=True, default=None, blank=True),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='telefono',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='text',
            field=models.TextField(null=True, default=None, blank=True),
        ),
    ]
