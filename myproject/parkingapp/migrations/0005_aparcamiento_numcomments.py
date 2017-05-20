# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parkingapp', '0004_auto_20170518_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='aparcamiento',
            name='numcomments',
            field=models.IntegerField(default=None, blank=True, null=True),
        ),
    ]
