# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parkingapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaginaUsuario',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
                ('usuarioCreador', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='accesibilidad',
            field=models.IntegerField(),
        ),
        migrations.AddField(
            model_name='paginausuario',
            name='aparcamientoSelec',
            field=models.ForeignKey(to='parkingapp.Aparcamiento'),
        ),
    ]
