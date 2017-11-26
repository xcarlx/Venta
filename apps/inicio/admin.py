# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from .models import Usuario, Menu, Permiso

# Register your models here.
class UsuarioInline(admin.StackedInline):
    model = Usuario
    can_delete = False
    verbose_name_plural = 'usuario'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UsuarioInline, )

class MenuAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    list_display = ('nombre','orden','url','icono','menu_padre',)
    list_display_links = ('nombre',)
    list_filter = ('menu_padre',)
    search_fields = ['nombre']

class PermisoAdmin(admin.ModelAdmin):
	empty_value_display = '-'
	list_display = ('usuario', 'menu','activo')
	list_display_links = ('usuario',)
	list_filter = ('usuario',)
	search_fields = ['usuario']
admin.site.register(Permiso, PermisoAdmin)




# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Menu, MenuAdmin)