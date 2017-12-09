from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DeleteView, TemplateView

from ..models import Usuario, Menu, Permiso
from ..forms import UserCreationForm
from ..formstotal import usuario

@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = "usuario/usuario.html"



@method_decorator(login_required, name='dispatch')
class JsonView(View):
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
        contact_list = User.objects.all().order_by("-id")
        if len(sort)>0:
            contact_list = User.objects.all().order_by(order+sort)
        if len(search)>0:
            if len(sort) == 0:
                sort='id'
            contact_list = User.objects.filter(
                Q(username__icontains = search)
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
            usua = Usuario.objects.get(user=dato)
            datadic ={}
            datadic['id'] = dato.id
            datadic['id1'] = usua.id
            datadic['usuario'] = dato.username
            datadic['password'] = dato.password
            lista.append(datadic)
        dic['total'] = contact_list.count()
        dic['rows'] = lista
        return JsonResponse(dic)


@method_decorator(login_required, name='dispatch')
class CreateUdateFormView(View):
    template_name = 'usuario/usuario_formulario.html'
    form_class = UserCreationForm
    form_class1 = usuario.UsuarioForm
    def get(self, request, *args, **kwargs):
        ids = int(self.kwargs['id'])
        iduser = int(self.kwargs['id1'])
        if ids == 0:
            form = self.form_class()
            form1 = self.form_class1()
        else:
            objeto = User.objects.get(pk=ids)
            objeto1 = Usuario.objects.get(pk=iduser)
            form = self.form_class(instance=objeto)
            form1 = self.form_class1(instance=objeto1)
        return render(request, self.template_name, {'form': form,'form1': form1})

    def post(self, request, *args, **kwargs):
        ids = int(self.kwargs['id'])
        iduser = int(self.kwargs['id1'])
        if ids == 0 and iduser == 0:
            form = self.form_class(request.POST)
            form1 = self.form_class1(request.POST)
        else:
            objeto = User.objects.get(pk=ids)
            objeto1 = Usuario.objects.get(pk=iduser)
            form = self.form_class(request.POST,instance=objeto)
            form1 = self.form_class1(request.POST,instance=objeto1)

        dic = {"estado":False, "mensaje":"No se guardo !!!"}
        if form.is_valid() and form1.is_valid():
            dic['estado'] = True
            dic['mensaje'] = "Guardado Correctamente"
            user = form.save()
            usuario = form1.save(commit=False)
            usuario.user= user
            usuario.save()
            if ids != 0 and iduser != 0:
                usuario.permisos.clear()
            for menu in form1.cleaned_data['permisos']:
                permiso = Permiso(
                    usuario = usuario,
                    menu = menu,
                    activo=True,
                )
                permiso.save()

            return JsonResponse(dic)

        return render(request, self.template_name, {'form': form,'form1': form1})



class SuccesEliminar(View):
    def get(self, response):
        dic = {}
        dic['estado'] = True
        dic['mensaje'] = "Eliminado Correctamente"
        return JsonResponse(dic)

class EliminarView(DeleteView):
    model = User
    template_name = 'usuario/usuario_eliminar_formulario.html'
    success_url = reverse_lazy('usuario-succes-eliminar')