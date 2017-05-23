# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('parkingapp', '0011_auto_20170522_2229'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estilo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('tamano', models.IntegerField(blank=True, null=True, default=None)),
                ('color', models.CharField(max_length=30)),
                ('usuario', models.OneToOneField(blank=True, to=settings.AUTH_USER_MODEL, null=True, default=None)),
            ],
        ),
    ]
