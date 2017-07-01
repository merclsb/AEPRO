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
    detalle_resultado_fda,
    detalle_resultado_cep,
	)
urlpatterns = [
	#Analisis-FBV
    url(r'^$', inicio, name='inicio'),
    url(r'^analisis/crear/$', analisis_model_form_crear, name='crear_analisis'),
    
    #url(r'^analisis/list/$', analisis_list, name='analisis_list'),
    url(r'^analisis/listcbv/$', AnalisisListView.as_view(), name='analisis_listcbv'),
    url(r'^analisis/detailcbv/(?P<pk>\d+)$', AnalisisDetailView.as_view(), name='analisis_detailcbv'),
    # url(r'^analisis/createcbv/$', AnalisisCreateView.as_view(), name='analisis_createcbv'),
    url(r'^analisis/updatecbv/(?P<pk>\d+)$', AnalisisUpdateView.as_view(), name='analisis_updatecbv'),
    url(r'^analisis/deletecbv/(?P<pk>\d+)$', AnalisisDeleteView.as_view(), name='analisis_deletecbv'),
    url(r'^resultado_detail_fda/(?P<pk>\d+)/$', detalle_resultado_fda, name='detalle_resultado_fda'),  
    url(r'^resultado_detail_cep/(?P<pk>\d+)/$', detalle_resultado_cep, name='detalle_resultado_cep'),  

    #otros
    url(r'^contacto/$', contacto, name='contacto'),
]