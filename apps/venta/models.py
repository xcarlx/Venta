# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from ..producto.models import Producto
from ..personas.models import Persona


class Venta(models.Model):
    BOLETA = 'B'
    FACTURA = 'F'
    TICKET = 'T'
    DOCUMENTO_CHOICES = (
        (BOLETA, 'Boleta'),
        (FACTURA, 'Factura'),
        (TICKET, 'Ticket'),
    )
    documento = models.CharField(max_length=1, choices=DOCUMENTO_CHOICES, default=BOLETA, )
    serie = models.CharField(max_length=2)
    numero = models.CharField(max_length=4)
    fecha = models.DateField(auto_now_add=True)
    persona = models.ForeignKey(Persona)
    total = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    pago = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    detalleventas = models.ManyToManyField(Producto, through='DetalleVenta', through_fields=('venta','producto',))


    def __unicode__(self):
        return "%s %s-%s || %s" % (self.documento, self.serie, self.numero, self.persona.nombreCompleto())



class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta)
    producto = models.ForeignKey(Producto)
    precio = models.DecimalField(max_digits=14, decimal_places=2)
    descuento = models.DecimalField(max_digits=14, decimal_places=2)
    cantidad = models.SmallIntegerField()