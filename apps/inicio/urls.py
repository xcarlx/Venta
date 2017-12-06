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
from .views import homeView, LoginView,PersonaEliminarView, \
    LogoutView,JsonPersonaView,PersonaFormView,JsonUbigeo,SuccesEliminar
from django.conf.urls import url

urlpatterns = [
    url(r'^$', homeView.as_view(), name='home'),
    url(r'^accounts/login/', LoginView.as_view(), name='login'),
    url(r'^accounts/logout/', LogoutView.as_view(), name='logout'),

    url(r'^persona/lista/', JsonPersonaView.as_view(), name='lista-persona'),
    url(r'^persona/formulario/(?P<id>[0-9]+)/', PersonaFormView.as_view(), name='persona-formulario'),
    url(r'^persona/eliminar/(?P<pk>[0-9]+)/', PersonaEliminarView.as_view(), name='persona-eliminar'),
    url(r'^persona/eliminar/success/', SuccesEliminar.as_view(), name='persona-succes-eliminar'),
    url(r'^persona/ubigeo/(?P<tipo>\w+)/(?P<id>[0-9]+)/', JsonUbigeo.as_view(), name='persona-ubigeo'),

]