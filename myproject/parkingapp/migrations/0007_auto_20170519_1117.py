# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parkingapp', '0006_auto_20170519_0837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aparcselect',
            name='fechaSelect',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='paginausuario',
            name='titulo',
            field=models.CharField(default=None, blank=True, null=True, max_length=50),
        ),
    ]
