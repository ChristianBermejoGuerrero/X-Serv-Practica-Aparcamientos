# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parkingapp', '0010_auto_20170520_0929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aparcamiento',
            name='numcomments',
            field=models.IntegerField(default=0, blank=True, null=True),
        ),
    ]
