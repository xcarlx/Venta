"""venta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from .viewstotal import marca,modelo, categoria, producto

urlpatterns = [

    #Producto
    url(r'^inicio/', producto.HomeView.as_view(), name='producto-home'),
    url(r'^lista/', producto.JsonView.as_view(), name='producto-lista'),
    url(r'^formulario/(?P<id>[0-9]+)/', producto.FormView.as_view(), name='producto-formulario'),
    url(r'^eliminar/(?P<pk>[0-9]+)/', producto.EliminarView.as_view(), name='producto-eliminar'),
    url(r'^success/', producto.SuccesEliminar.as_view(), name='producto-succes-eliminar'),

    #Marca
    url(r'^marca/inicio/', marca.HomeView.as_view(), name='marca-home'),
    url(r'^marca/lista/', marca.JsonView.as_view(), name='marca-lista'),
    url(r'^marca/formulario/(?P<id>[0-9]+)/', marca.FormView.as_view(), name='marca-formulario'),
    url(r'^marca/eliminar/(?P<pk>[0-9]+)/', marca.EliminarView.as_view(), name='marca-eliminar'),
    url(r'^marca/success/', marca.SuccesEliminar.as_view(), name='marca-succes-eliminar'),

    #Modelo
    url(r'^modelo/inicio/', modelo.HomeView.as_view(), name='modelo-home'),
    url(r'^modelo/lista/', modelo.JsonView.as_view(), name='modelo-lista'),
    url(r'^modelo/formulario/(?P<id>[0-9]+)/', modelo.FormView.as_view(), name='modelo-formulario'),
    url(r'^modelo/eliminar/(?P<pk>[0-9]+)/', modelo.EliminarView.as_view(), name='modelo-eliminar'),
    url(r'^modelo/success/', modelo.SuccesEliminar.as_view(), name='modelo-succes-eliminar'),

    #Categoria
    url(r'^categoria/inicio/', categoria.HomeView.as_view(), name='categoria-home'),
    url(r'^categoria/lista/', categoria.JsonView.as_view(), name='categoria-lista'),
    url(r'^categoria/formulario/(?P<id>[0-9]+)/', categoria.FormView.as_view(), name='categoria-formulario'),
    url(r'^categoria/eliminar/(?P<pk>[0-9]+)/', categoria.EliminarView.as_view(), name='categoria-eliminar'),
    url(r'^categoria/success/', categoria.SuccesEliminar.as_view(), name='categoria-succes-eliminar'),

]
