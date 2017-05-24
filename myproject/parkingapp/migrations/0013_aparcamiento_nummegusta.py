# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parkingapp', '0012_estilo'),
    ]

    operations = [
        migrations.AddField(
            model_name='aparcamiento',
            name='nummegusta',
            field=models.IntegerField(null=True, blank=True, default=0),
        ),
    ]
