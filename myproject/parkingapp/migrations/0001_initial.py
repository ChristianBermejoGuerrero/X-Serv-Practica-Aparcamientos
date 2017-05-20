# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aparcamiento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('link', models.CharField(max_length=100)),
                ('latitud', models.IntegerField()),
                ('longitud', models.IntegerField()),
                ('descripcion', models.TextField()),
                ('accesibilidad', models.BooleanField()),
                ('barrio', models.CharField(max_length=50)),
                ('telefono', models.IntegerField()),
                ('email', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('aparcamiento', models.ForeignKey(to='parkingapp.Aparcamiento')),
            ],
        ),
        migrations.CreateModel(
            name='Distrito',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='aparcamiento',
            name='distrito',
            field=models.ForeignKey(to='parkingapp.Distrito'),
        ),
    ]
