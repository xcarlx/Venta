# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Persona, Ubigeo


class PersonaAdmin(admin.ModelAdmin):
	pass
admin.site.register(Persona, PersonaAdmin)

class UbigeoAdmin(admin.ModelAdmin):
	empty_value_display = '-empty-'
	list_display = ('cod_dep', 'cod_pro','cod_dis','nombre')
	list_display_links = ('nombre',)
	list_filter = ('cod_dep',)
	search_fields = ['nombre']
admin.site.register(Ubigeo, UbigeoAdmin)

# Register your models here.

