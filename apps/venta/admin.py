# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from ..venta.models import Venta, DetalleVenta

admin.site.register(Venta)



class DetalleVentaAdmin(admin.ModelAdmin):
	empty_value_display = '-empty-'
	list_display = ("producto", "venta",)
	list_display_links = ("producto", "venta",)
	list_filter = ('producto',)
	search_fields = "__all__",
admin.site.register(DetalleVenta, DetalleVentaAdmin)