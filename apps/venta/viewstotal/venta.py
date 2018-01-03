# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.forms import formset_factory, inlineformset_factory

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DeleteView, TemplateView

from apps.producto.models import Producto
from ..formstotal.venta import VentaForm, DetalleVentaForm
from ..models import Venta, DetalleVenta


@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = "venta/home.html"


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
        contact_list = Venta.objects.all().order_by("-id")
        if len(sort)>0:
            contact_list = Venta.objects.all().order_by(order+sort)
        if len(search)>0:
            if len(sort) == 0:
                sort='id'
            contact_list = Venta.objects.filter(
                Q(serie__icontains = search) |
                Q(numero__icontains = search)
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
            dicobjec['documento'] = objeto.get_documento_display()
            dicobjec['serie'] = objeto.serie
            dicobjec['numero'] = objeto.numero
            dicobjec['fecha'] = objeto.fecha.strftime("%d/%m/%Y")
            dicobjec['persona__nombre'] = objeto.persona.nombreCompleto()
            dicobjec['total'] = objeto.total
            lista.append(dicobjec)
        dic['total'] = contact_list.count()
        dic['rows'] = lista

        return JsonResponse(dic)



@method_decorator(login_required, name='dispatch')
class FormView(View):
    template_name = 'venta/formulario.html'
    form_class = VentaForm
    form_class1 = inlineformset_factory(Venta, DetalleVenta,form = DetalleVentaForm, extra=1)

    def get(self, request, *args, **kwargs):
        ids = int(self.kwargs['id'])
        if ids == 0:
            form1 = self.form_class1()
            form = self.form_class()
        else:
            objeto = Venta.objects.get(pk=ids)
            form = self.form_class(instance=objeto)
            form1 = self.form_class1(instance=objeto)
        return render(request, self.template_name, {'form': form, 'form1': form1})

    def post(self, request, *args, **kwargs):
        ids = int(self.kwargs['id'])
        if ids == 0:
            form = self.form_class(request.POST, request.FILES)
            form1 = self.form_class1(request.POST, request.FILES)
        else:
            objeto = Venta.objects.get(pk=ids)
            form = self.form_class(request.POST, request.FILES, instance=objeto)
            form1 = self.form_class1(request.POST,instance=objeto)
        dic = {"estado":False, "mensaje":"No se guardo !!!"}
        if form.is_valid() and form1.is_valid():
            dic['estado'] = True
            dic['mensaje'] = "Guardado Correctamente"
            venta =  form.save()
            form1.instance = venta
            form1.save()
            ActualizarDatosVenta(venta)
            return JsonResponse(dic)

        return render(request, self.template_name, {'form': form, 'form1': form1})


@method_decorator(login_required, name='dispatch')
class SuccesEliminar(View):
    def get(self, response):
        dic = {}
        dic['estado'] = True
        dic['mensaje'] = "Eliminado Correctamente"
        return JsonResponse(dic)

@method_decorator(login_required, name='dispatch')
class EliminarView(DeleteView):
    model = Venta
    template_name = 'venta/eliminar_formulario.html'
    success_url = reverse_lazy('modelo-succes-eliminar')



def ActualizarDatosVenta(venta):
    total=0
    for detalle in venta.detalleventa_set.all():
        total = total + (detalle.precio * detalle.cantidad)-detalle.descuento
    venta.total = total
    venta.save()


@method_decorator(login_required, name='dispatch')
class JsonProductoView(View):
    def get(self, request, *args,**kwargs):
        objeto = Producto.objects.get(pk = kwargs['pk'])
        dic = {}
        dic['id'] = objeto.id
        dic['codigo'] = objeto.codigo
        dic['descripcion'] = objeto.descripcion
        dic['categoria__nombre'] = objeto.categoria.nombre
        dic['modelo__marca__nombre'] = objeto.modelo.marca.nombre
        dic['modelo__nombre'] = objeto.modelo.nombre
        dic['precio'] = objeto.precio
        dic['imagen'] = objeto.imagen.url if objeto.imagen != "" else ""
        return JsonResponse(dic)




