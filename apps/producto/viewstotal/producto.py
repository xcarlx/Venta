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

from ..formstotal.producto import ProductoForm
from ..models import Producto

@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = "producto/home.html"


# Create your views here.
@method_decorator(login_required, name='dispatch')
class JsonView(View):
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
        contact_list = Producto.objects.all().order_by("-id")
        if len(sort)>0:
            contact_list = Producto.objects.all().order_by(order+sort)
        if len(search)>0:
            if len(sort) == 0:
                sort='id'
            contact_list = Producto.objects.filter(
                Q(codigo__icontains = search) |
                Q(descripcion__icontains = search) |
                Q(categoria__nombre__icontains = search)|
                Q(modelo__nombre__icontains = search)|
                Q(modelo__marca__nombre__icontains = search)
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
        for objeto in contacts:
            dicobjec ={}
            dicobjec['id'] = objeto.id
            dicobjec['codigo'] = objeto.codigo
            dicobjec['descripcion'] = objeto.descripcion
            dicobjec['categoria__nombre'] = objeto.categoria.nombre
            dicobjec['modelo__marca__nombre'] = objeto.modelo.marca.nombre
            dicobjec['modelo__nombre'] = objeto.modelo.nombre
            dicobjec['precio'] = objeto.precio
            dicobjec['imagen'] = objeto.imagen.url if objeto.imagen != "" else ""
            lista.append(dicobjec)
        dic['total'] = contact_list.count()
        dic['rows'] = lista

        return JsonResponse(dic)



@method_decorator(login_required, name='dispatch')
class FormView(View):
    template_name = 'producto/formulario.html'
    form_class = ProductoForm

    def get(self, request, *args, **kwargs):
        ids = int(self.kwargs['id'])
        if ids == 0:
            form = self.form_class()
        else:
            objeto = Producto.objects.get(pk=ids)
            form = self.form_class(instance=objeto)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        ids = int(self.kwargs['id'])
        if ids == 0:
            form = self.form_class(request.POST)
        else:
            objeto = Producto.objects.get(pk=ids)
            form = self.form_class(request.POST,instance=objeto)
        dic = {"estado":False, "mensaje":"No se guardo !!!"}
        if form.is_valid():
            dic['estado'] = True
            dic['mensaje'] = "Guardado Correctamente"
            form.save()
            return JsonResponse(dic)

        return render(request, self.template_name, {'form': form})



class SuccesEliminar(View):
    def get(self, response):
        dic = {}
        dic['estado'] = True
        dic['mensaje'] = "Eliminado Correctamente"
        return JsonResponse(dic)

class EliminarView(DeleteView):
    model = Producto
    template_name = 'producto/eliminar_formulario.html'
    success_url = reverse_lazy('modelo-succes-eliminar')