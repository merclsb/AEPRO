# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import (
	inicio,#
	analisis_model_form_crear,
	AnalisisListView,
	AnalisisDetailView,
	AnalisisDeleteView,
	AnalisisUpdateView,
	contacto,
	)
urlpatterns = [
	#Analisis-FBV
    url(r'^$', inicio, name='inicio'),
    url(r'^crear/$', analisis_model_form_crear, name='crear_analisis'),
    
    #url(r'^analisis/list/$', analisis_list, name='analisis_list'),
    url(r'^analisis/listcbv/$', AnalisisListView.as_view(), name='analisis_listcbv'),
    url(r'^analisis/detailcbv/(?P<pk>\d+)$', AnalisisDetailView.as_view(), name='analisis_detailcbv'),
    # url(r'^analisis/createcbv/$', AnalisisCreateView.as_view(), name='analisis_createcbv'),
    url(r'^analisis/updatecbv/(?P<pk>\d+)$', AnalisisUpdateView.as_view(), name='analisis_updatecbv'),
    url(r'^analisis/deletecbv/(?P<pk>\d+)$', AnalisisDeleteView.as_view(), name='analisis_deletecbv'),
    #otros
    url(r'^contacto/$', contacto, name='contacto'),
]