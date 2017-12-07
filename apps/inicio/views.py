# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.base import View

from ..personas.models import Persona, Ubigeo
from .models import Permiso
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import AuthenticationForm
from django.contrib.auth import authenticate, login,logout


# Create your views here.
@method_decorator(login_required, name='dispatch')
class homeView(TemplateView):
    template_name = "inicio.html"

    # def get_context_data(self, **kwargs):
    #     context = super(homeView, self).get_context_data(**kwargs)
    #     # here's the difference:
    #     context['personas'] = Persona.objects.all()
    #     return context

class LoginView(View):
    form_class = AuthenticationForm
    template_name = 'login.html'
    def get(self, request):
        return render(request,self.template_name,{"form" : self.form_class})
    def post(self, request):
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = authenticate(request, username=username, password=password)
        menus = Permiso.objects.filter(activo=True)
        lista = []
        for m in menus:
            dato = {'hijo':m.menu.nombre, 'url':m.menu.url, 'icono':m.menu.icono, 'padre':m.menu.menu_padre.nombre}
            lista.append(dato)
        if user is not None:
            request.session['menu']=lista
            login(request, user)
            return redirect('/')
        else:
            return render(request, self.template_name, {"form": self.form_class})


class LogoutView(View):
    def get(self, requets):
        logout(requets)
        return redirect('/')

@method_decorator(login_required, name='dispatch')
class JsonUbigeo(View):
    def get(self, request,  *args, **kwargs):
        tipo = kwargs['tipo']
        dic = {}
        lista = []
        ids = kwargs['id']
        if tipo=="provincia":
            departamento = Ubigeo.objects.get(pk = ids)
            ubigeos = Ubigeo.objects.filter(cod_dep=departamento.cod_dep,cod_dis='00').exclude(cod_pro='00')
            for ubigeo in ubigeos:
                dicubigeo = {}
                dicubigeo['nombre'] = ubigeo.nombre
                dicubigeo['cod_pro'] = ubigeo.cod_pro
                dicubigeo['idprovincia'] = ubigeo.id
                lista.append(dicubigeo)
            dic['ubigeo'] = lista
            return JsonResponse(dic)
        else:
            distrito = Ubigeo.objects.get(pk=ids)
            ubigeos = Ubigeo.objects.filter(cod_pro=distrito.cod_pro,cod_dep=distrito.cod_dep).exclude(cod_dis='00')
            for ubigeo in ubigeos:
                dicubigeo = {}
                dicubigeo['nombre'] = ubigeo.nombre
                dicubigeo['cod_dis'] = ubigeo.cod_dis
                dicubigeo['iddistrito'] = ubigeo.id
                lista.append(dicubigeo)
            dic['ubigeo'] = lista
            return JsonResponse(dic)

