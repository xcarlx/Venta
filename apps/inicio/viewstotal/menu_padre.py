from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DeleteView, TemplateView

from ..formstotal.menu import MenuPadreForm
from ..models import Menu

@method_decorator(login_required, name='dispatch')
class MenuHomeView(TemplateView):
    template_name = "menu_padre/menu.html"

@method_decorator(login_required, name='dispatch')
class JsonMenuView(View):
    def get(self, request, *args, **kwargs):
        order = str(request.GET.get('order'))
        offset = int(request.GET.get('offset',0))
        limit = int(request.GET.get('limit',10))
        search = str(request.GET.get('search',''))
        sort = str(request.GET.get('sort',''))
        if order == 'desc':
            order = str('-')
        else:
            order = str('')
        contact_list = Menu.objects.filter(menu_padre=None).order_by("-orden")
        if len(sort)>0:
            contact_list = Menu.objects.filter(menu_padre=None).order_by(order+sort)
        if len(search)>0:
            if len(sort) == 0:
                sort='orden'
            contact_list = Menu.objects.filter(
                Q(nombre__icontains = search, menu_padre=None) |
                Q(url__icontains = search, menu_padre=None) |
                Q(icono__icontains = search, menu_padre=None)
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
        for dato in contacts:
            datadic ={}
            datadic['id'] = dato.id
            datadic['nombre'] = dato.nombre
            datadic['orden'] = dato.orden
            datadic['url'] = dato.url
            datadic['icono'] = dato.icono
            datadic['menu_padre'] = dato.menu_padre.nombre if dato.menu_padre is not None else ""
            lista.append(datadic)
        dic['total'] = contact_list.count()
        dic['rows'] = lista
        return JsonResponse(dic)


@method_decorator(login_required, name='dispatch')
class MenuFormView(View):
    template_name = 'menu_padre/menu_formulario.html'
    form_class = MenuPadreForm
    def get(self, request, *args, **kwargs):
        ids = int(self.kwargs['id'])
        if ids == 0:
            form = self.form_class()
        else:
            objeto = Menu.objects.get(pk=ids)
            form = self.form_class(instance=objeto)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        ids = int(self.kwargs['id'])
        if ids == 0:
            form = self.form_class(request.POST)
        else:
            objeto = Menu.objects.get(pk=ids)
            form = self.form_class(request.POST,instance=objeto)
        dic = {"estado":False, "mensaje":"No se guardo !!!"}
        if form.is_valid():
            dic['estado'] = True
            dic['mensaje'] = "Guardado Correctamente"
            form.save()
            return JsonResponse(dic)

        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class SuccesMenuEliminar(View):
    def get(self, response):
        dic = {}
        dic['estado'] = True
        dic['mensaje'] = "Eliminado Correctamente"
        return JsonResponse(dic)

@method_decorator(login_required, name='dispatch')
class MenuEliminarView(DeleteView):
    model = Menu
    template_name = 'menu_padre/menu_eliminar_formulario.html'
    success_url = reverse_lazy('menu-padre-succes-eliminar')