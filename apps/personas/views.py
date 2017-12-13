# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DeleteView, TemplateView

from .forms import PersonaInicioForm
from .models import Persona



@method_decorator(login_required, name='dispatch')
class HomePersona(TemplateView):
    template_name = "persona_inicio.html"

    # def get_context_data(self, **kwargs):
    #     context = super(homeView, self).get_context_data(**kwargs)
    #     # here's the difference:
    #     context['personas'] = Persona.objects.all()
    #     return context


# Create your views here.
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
            if len(sort) == 0:
                sort='id'
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
            person['nacimiento'] = persona.nacimiento.strftime("%d/%m/%Y") if persona.nacimiento is not None else ""
            person['lugar'] = persona.LugarNacimineto()
            lista.append(person)
        dic['total'] = contact_list.count()
        dic['rows'] = lista

        return JsonResponse(dic)



@method_decorator(login_required, name='dispatch')
class PersonaFormView(View):
    template_name = 'formulariopersona.html'
    form_class = PersonaInicioForm

    def get(self, request, *args, **kwargs):
        ids = int(self.kwargs['id'])
        if ids == 0:
            form = self.form_class()
        else:
            persona = Persona.objects.get(pk=ids)
            dep = persona.IdsUbigeo()['departamento']
            pro = persona.IdsUbigeo()['provincia']
            dis = persona.IdsUbigeo()['distrito']
            initial = {'departamento': dep,'provincia':pro, 'distrito':dis}
            form = self.form_class(instance=persona, initial=initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        ids = int(self.kwargs['id'])
        if ids == 0:
            form = self.form_class(request.POST)
        else:
            persona = Persona.objects.get(pk=ids)
            dep = persona.IdsUbigeo()['departamento']
            pro = persona.IdsUbigeo()['provincia']
            dis = persona.IdsUbigeo()['distrito']
            initial = {'departamento': dep, 'provincia': pro, 'distrito': dis}
            form = self.form_class(request.POST,instance=persona,initial=initial)
        dic = {"estado":False, "mensaje":"No se guardo !!!"}
        if form.is_valid():
            dic['estado'] = True
            dic['mensaje'] = "Guardado Correctamente"
            form.save()
            return JsonResponse(dic)

        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class SuccesEliminar(View):
    def get(self, response):
        dic = {}
        dic['estado'] = True
        dic['mensaje'] = "Eliminado Correctamente"
        return JsonResponse(dic)

@method_decorator(login_required, name='dispatch')
class PersonaEliminarView(DeleteView):
    model = Persona
    template_name = 'eliminarpersona.html'
    success_url = reverse_lazy('persona-succes-eliminar')

