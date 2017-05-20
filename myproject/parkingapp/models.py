from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Distrito(models.Model):
    nombre = models.CharField(max_length=50,null=True, blank=True, default=None)

class Aparcamiento(models.Model):
    nombre = models.CharField(max_length=50,null=True, blank=True, default=None)
    link = models.CharField(max_length=100,null=True, blank=True, default=None)
    clasevial = models.CharField(max_length=100,null=True, blank=True, default=None)
    nombrevia = models.CharField(max_length=100,null=True, blank=True, default=None)
    numvia = models.CharField(max_length=10,null=True, blank=True, default=None) #algunas tienen letras
    numcomments = models.IntegerField(null=True, blank=True, default=None)
    latitud = models.FloatField(null=True, blank=True, default=None)
    longitud = models.FloatField(null=True, blank=True, default=None)
    descripcion = models.TextField(null=True, blank=True, default=None)
    accesibilidad = models.IntegerField(null=True, blank=True, default=None)
    barrio = models.CharField(max_length=50,null=True, blank=True, default=None)
    distrito = models.ForeignKey(Distrito,null=True, blank=True, default=None)
    telefono = models.CharField(max_length=12,null=True, blank=True, default=None)
    email = models.CharField(max_length=50,null=True, blank=True, default=None)

class Comentario(models.Model):
    text = models.TextField(null=True, blank=True, default=None)
    aparcamiento = models.ForeignKey(Aparcamiento,null=True, blank=True, default=None)

class PaginaUsuario (models.Model):
    usuario = models.OneToOneField(User,null=True, blank=True, default=None) #cada paginausuario solo puede ser de un usuario
    titulo = models.CharField(max_length=50,null=True, blank=True, default=None)

class AparcSelect (models.Model):
    usuario = models.ForeignKey(User,null=True, blank=True, default=None)
    pagUsuario = models.ForeignKey(PaginaUsuario,null=True, blank=True, default=None)
    aparcamiento = models.ForeignKey(Aparcamiento,null=True, blank=True, default=None)
    fechaSelect = models.DateTimeField(auto_now_add=True) #inicializa a la fecha de su .save()
