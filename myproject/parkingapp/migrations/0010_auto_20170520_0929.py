# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parkingapp', '0009_auto_20170519_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aparcselect',
            name='fechaSelect',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
