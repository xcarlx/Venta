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
from ..inicio import views
from ..inicio.viewstotal import menu_padre
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.homeView.as_view(), name='home'),
    url(r'^accounts/login/', views.LoginView.as_view(), name='login'),
    url(r'^accounts/logout/', views.LogoutView.as_view(), name='logout'),
    url(r'^inicio/ubigeo/(?P<tipo>\w+)/(?P<id>[0-9]+)/', views.JsonUbigeo.as_view(), name='persona-ubigeo'),

    # MENUS PADRE
    url(r'^menu/padre/inicio/', menu_padre.MenuHomeView.as_view(), name='menu-padre-home'),
    url(r'^menu/padre/lista/', menu_padre.JsonMenuView.as_view(), name='menu-padre-lista'),
    url(r'^menu/padre/formulario/(?P<id>[0-9]+)/', menu_padre.MenuFormView.as_view(), name='menu-padre-formulario'),
    url(r'^menu/padre/eliminar/(?P<pk>[0-9]+)/', menu_padre.MenuEliminarView.as_view(), name='menu-padre-eliminar'),
    url(r'^menu/padre/eliminar/success/', menu_padre.SuccesMenuEliminar.as_view(), name='menu-padre-succes-eliminar'),

]