# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from ..personas.models import Persona

# Create your models here.

class Menu(models.Model):
    nombre = models.CharField(max_length=100)
    orden = models.SmallIntegerField()
    url = models.CharField(max_length=200, blank=True, null=True)
    icono = models.CharField(max_length=50, blank=True, null=True)
    menu_padre = models.ForeignKey("self", related_name='+',blank=True, null=True)


    def __unicode__(self):
        return self.nombre

class Usuario(models.Model):
    ADMINISTRADO = 'A'
    OPERADOR = 'O'
    CLIENTE = 'C'
    TIPO_CHOICES = (
        (ADMINISTRADO, 'Administrador'),
        (OPERADOR, 'Operador'),
        (CLIENTE, 'Cliente'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(max_length=1, choices=TIPO_CHOICES, default=ADMINISTRADO, )
    persona = models.ForeignKey(Persona, blank=True, null=True)
    permisos = models.ManyToManyField(Menu, through='Permiso', through_fields=('usuario','menu'))

    def __unicode__(self):
        return self.user.username


class Permiso(models.Model):
    usuario = models.ForeignKey(Usuario)
    menu = models.ForeignKey(Menu)
    activo = models.BooleanField(default=True)
