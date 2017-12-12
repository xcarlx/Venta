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
from .viewstotal import marca

urlpatterns = [

    url(r'^marca/inicio/', marca.HomeView.as_view(), name='marca-home'),
    url(r'^marca/lista/', marca.JsonView.as_view(), name='marca-lista'),
    url(r'^marca/formulario/(?P<id>[0-9]+)/', marca.FormView.as_view(), name='marca-formulario'),
    url(r'^marca/eliminar/(?P<pk>[0-9]+)/', marca.EliminarView.as_view(), name='marca-eliminar'),
    url(r'^marca/success/', marca.SuccesEliminar.as_view(), name='marca-succes-eliminar'),

]
