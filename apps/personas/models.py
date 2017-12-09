# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse


class Ubigeo(models.Model):
    cod_dep = models.CharField(max_length=2)
    cod_pro = models.CharField(max_length=2)
    cod_dis = models.CharField(max_length=2)
    nombre = models.CharField(max_length=100)

    def __unicode__(self):
        return "%s" % (self.nombre)


class Persona(models.Model):
    FEMENINO = 'F'
    MASCULINO = 'M'
    SEXOL_CHOICES = (
        (FEMENINO, 'Femenino'),
        (MASCULINO, 'Masculino'),
    )
    nombre = models.CharField(max_length=50)
    paterno = models.CharField(max_length=50)
    materno = models.CharField(max_length=50)
    nacimiento = models.DateField(blank=True, null=True)
    ubigeo = models.ForeignKey(Ubigeo)
    sexo = models.CharField(max_length=1, choices=SEXOL_CHOICES, default=MASCULINO, )

    def __unicode__(self):
        return "%s %s" % (self.nombre, self.paterno)

    def nombreCompleto(self):
        return self.nombre + ' ' + self.paterno + ' ' + self.materno

    def LugarNacimineto(self):
        coddep = self.ubigeo.cod_dep
        codpro = self.ubigeo.cod_pro
        departamento = Ubigeo.objects.get(cod_dep=coddep, cod_pro='00', cod_dis='00')
        provincia = Ubigeo.objects.get(cod_dep=coddep, cod_pro=codpro, cod_dis='00')
        return "%s - %s - %s" % (departamento.nombre, provincia.nombre, self.ubigeo.nombre)

    def IdsUbigeo(self):
        coddep = self.ubigeo.cod_dep
        codpro = self.ubigeo.cod_pro
        departamento = Ubigeo.objects.get(cod_dep=coddep, cod_pro='00', cod_dis='00')
        provincia = Ubigeo.objects.get(cod_dep=coddep, cod_pro=codpro, cod_dis='00')
        return {'departamento': departamento.id, 'provincia': provincia.id, 'distrito': self.ubigeo.id}
