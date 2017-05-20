# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('parkingapp', '0005_aparcamiento_numcomments'),
    ]

    operations = [
        migrations.CreateModel(
            name='AparcSelect',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('fechaSelect', models.DateField(auto_now=True)),
                ('aparcamiento', models.ForeignKey(null=True, to='parkingapp.Aparcamiento', blank=True, default=None)),
            ],
        ),
        migrations.RemoveField(
            model_name='paginausuario',
            name='aparcamientoSelec',
        ),
        migrations.RemoveField(
            model_name='paginausuario',
            name='nombre',
        ),
        migrations.RemoveField(
            model_name='paginausuario',
            name='usuarioCreador',
        ),
        migrations.AddField(
            model_name='paginausuario',
            name='titulo',
            field=models.CharField(max_length=32, blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='paginausuario',
            name='usuario',
            field=models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL, blank=True, default=None),
        ),
        migrations.AddField(
            model_name='aparcselect',
            name='pagUsuario',
            field=models.ForeignKey(null=True, to='parkingapp.PaginaUsuario', blank=True, default=None),
        ),
        migrations.AddField(
            model_name='aparcselect',
            name='usuario',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, blank=True, default=None),
        ),
    ]
