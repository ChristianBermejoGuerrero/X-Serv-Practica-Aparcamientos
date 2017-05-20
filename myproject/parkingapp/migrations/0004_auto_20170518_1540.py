# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parkingapp', '0003_auto_20170518_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aparcamiento',
            name='barrio',
            field=models.CharField(null=True, max_length=50, blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='distrito',
            field=models.ForeignKey(null=True, default=None, to='parkingapp.Distrito', blank=True),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='email',
            field=models.CharField(null=True, max_length=50, blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='link',
            field=models.CharField(null=True, max_length=100, blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='nombre',
            field=models.CharField(null=True, max_length=50, blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='telefono',
            field=models.CharField(null=True, max_length=12, blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='aparcamiento',
            field=models.ForeignKey(null=True, default=None, to='parkingapp.Aparcamiento', blank=True),
        ),
        migrations.AlterField(
            model_name='distrito',
            name='nombre',
            field=models.CharField(null=True, max_length=50, blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='paginausuario',
            name='aparcamientoSelec',
            field=models.ForeignKey(null=True, default=None, to='parkingapp.Aparcamiento', blank=True),
        ),
    ]
