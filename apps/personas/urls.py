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

from ..personas import views

urlpatterns = [
    # url(r'^$', homeView.as_view(), name='home')
    url(r'^home/', views.HomePersona.as_view(), name='persona-home'),
    url(r'^lista/', views.JsonPersonaView.as_view(), name='lista-persona'),
    url(r'^formulario/(?P<id>[0-9]+)/', views.PersonaFormView.as_view(), name='persona-formulario'),
    url(r'^eliminar/(?P<pk>[0-9]+)/', views.PersonaEliminarView.as_view(), name='persona-eliminar'),
    url(r'^eliminar/success/', views.SuccesEliminar.as_view(), name='persona-succes-eliminar'),
]