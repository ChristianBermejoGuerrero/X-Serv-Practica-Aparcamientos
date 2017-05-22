"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from parkingapp import views
from django.contrib.auth.views import login, logout


urlpatterns = [
    url(r'^$', views.showPrincipal, name='pagina principal'),
    url(r'^aparcamientos$', views.showAllParkings, name='pagina todos los aparcamientos'),
    url(r'^aparcamientos/(.+)$', views.showOneParking, name='pagina de un aparcamiento con su informacion'),
    # url(r'^(.+)/xml$', views.userxml, name='canal xml de aparcamientos seleccionados por ese usuario'),
    # url(r'^about$', views.about, name='pagina de informacion HTML, autoria y funcionamiento'),
    url(r'^uploadxml$', views.uploadxml, name='cargar el xml que contiene los datos'),
    url(r'^login$', views.login, name='log in'),
    url(r'^logout$', logout, {'next_page': '/'}, name='log out'),
    #url(r'^CSS$', views.userpage, name='css'),
    url(r'^(.+)$', views.showUserpage, name='pagina de usuario'),
    url(r'^admin/', include(admin.site.urls)),
]
