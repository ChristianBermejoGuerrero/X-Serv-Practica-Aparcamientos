# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parkingapp', '0007_auto_20170519_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='aparcamiento',
            name='clasevial',
            field=models.CharField(default=None, max_length=100, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='aparcamiento',
            name='nombrevia',
            field=models.CharField(default=None, max_length=100, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='aparcamiento',
            name='numvia',
            field=models.IntegerField(default=None, blank=True, null=True),
        ),
    ]
