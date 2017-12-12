# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'producto/{0}/{1}'.format(instance.codigo, filename)

class Marca(models.Model):
    nombre = models.CharField(max_length=50)

    def __unicode__(self):
        return "%s" % (self.nombre)

class Modelo(models.Model):
    nombre = models.CharField(max_length=50)
    marca = models.ForeignKey(Marca)

    def __unicode__(self):
        return "%s" % (self.nombre)

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __unicode__(self):
        return "%s" % (self.nombre)


class Producto(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=500, unique=True)
    categoria = models.ForeignKey(Categoria)
    modelo = models.ForeignKey(Modelo, blank=True, null=True)
    precio = models.DecimalField(max_digits=14, decimal_places=2)
    imagen = models.ImageField(upload_to=user_directory_path, height_field=200, width_field=200)

    def __unicode__(self):
        return "%s  |  %s" % (self.codigo, self.descripcion)


