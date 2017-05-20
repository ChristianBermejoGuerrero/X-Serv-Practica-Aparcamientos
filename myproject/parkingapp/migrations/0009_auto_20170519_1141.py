# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parkingapp', '0008_auto_20170519_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aparcamiento',
            name='numvia',
            field=models.CharField(null=True, blank=True, max_length=10, default=None),
        ),
    ]
