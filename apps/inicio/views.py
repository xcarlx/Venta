# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.base import View

from ..personas.models import Persona, Ubigeo
from .models import Permiso
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import AuthenticationForm
from django.contrib.auth import authenticate, login,logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.generic.edit import FormView, CreateView
from .forms import PersonaInicioForm
from django.db.models import Q

# Create your views here.
@method_decorator(login_required, name='dispatch')
class homeView(TemplateView):
    template_name = "inicio.html"

    # def get_context_data(self, **kwargs):
    #     context = super(homeView, self).get_context_data(**kwargs)
    #     # here's the difference:
    #     context['personas'] = Persona.objects.all()
    #     return context


@method_decorator(login_required, name='dispatch')
class JsonPersonaView(View):
    def get(self, request):
        order = str(request.GET.get('order'))
        offset = int(request.GET.get('offset',0))
        limit = int(request.GET.get('limit',10))
        search = str(request.GET.get('search',''))
        sort = str(request.GET.get('sort',''))
        if order == 'desc':
            order = str('-')
        else:
            order = str('')
        contact_list = Persona.objects.all().order_by("-id")
        if len(sort)>0:
            contact_list = Persona.objects.all().order_by(order+sort)
        if len(search)>0:
            contact_list = Persona.objects.filter(
                Q(nombre__icontains = search) |
                Q(materno__icontains = search) |
                Q(paterno__icontains = search)
            ).order_by(order + sort)
        paginator = Paginator(contact_list, limit)  # Show 25 contacts per page
        page = (offset/limit)+1
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
        dic = {}
        lista = []
        for persona in contacts:
            person ={}
            person['id'] = persona.id
            person['nombre'] = persona.nombre
            person['paterno'] = persona.paterno
            person['materno'] = persona.materno
            person['sexo'] = persona.get_sexo_display()
            person['lugar'] = persona.LugarNacimineto()
            lista.append(person)
        dic['total'] = contact_list.count()
        dic['rows'] = lista

        return JsonResponse(dic)

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
class PersonaFormView(View):
    template_name = 'formulariopersona.html'
    form_class = PersonaInicioForm
    success_url = '/thanks/'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect('/success/')

        return render(request, self.template_name, {'form': form})

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
