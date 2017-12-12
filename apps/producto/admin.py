# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Producto



class ProductoAdmin(admin.ModelAdmin):
	empty_value_display = '-empty-'
	list_display = ("codigo", "descripcion",)
	list_display_links = ("codigo", "descripcion",)
	list_filter = ('descripcion',)
	search_fields = "__all__",
admin.site.register(Producto, ProductoAdmin)