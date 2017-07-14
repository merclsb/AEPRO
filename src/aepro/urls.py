# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import (
	inicio,#
	analisis_model_form_crear,
	AnalisisListView,
	AnalisisDetailView,
	AnalisisDeleteView,
    AnalisisDeleteViewError,
    Analisis_FDA_UpdateView,
    Analisis_CEP_UpdateView,
	contacto,
    detalle_resultado_fda,
    detalle_resultado_cep,
    ValidarFichero,
	)
urlpatterns = [
	url(r'^$', inicio, name='inicio'),
    url(r'^analisis/crear/$', analisis_model_form_crear, name='crear_analisis'),
    
    #url(r'^analisis/list/$', analisis_list, name='analisis_list'),
    url(r'^analisis/listcbv/$', AnalisisListView.as_view(), name='analisis_listcbv'),
    url(r'^analisis/detailcbv/(?P<pk>\d+)$', AnalisisDetailView.as_view(), name='analisis_detailcbv'),
    # url(r'^analisis/createcbv/$', AnalisisCreateView.as_view(), name='analisis_createcbv'),
    url(r'^analisis/update_fda/(?P<pk>\d+)$', Analisis_FDA_UpdateView.as_view(), name='analisis_fda_update'),
    #url(r'^analisis/update_fda/(?P<pk>\d+)$', actualizar_fda, name='analisis_fda_update'),
    url(r'^analisis/update_cep/(?P<pk>\d+)$', Analisis_CEP_UpdateView.as_view(), name='analisis_cep_update'),
    url(r'^analisis/deletecbv/(?P<pk>\d+)$', AnalisisDeleteView.as_view(), name='analisis_deletecbv'),
    url(r'^analisis/deletecbverror/(?P<pk>\d+)$', AnalisisDeleteViewError.as_view(), name='analisis_deletecbv_error'),
    url(r'^analisis/resultado_detail_fda/(?P<pk>\d+)/$', detalle_resultado_fda, name='detalle_resultado_fda'),  
    url(r'^analisis/resultado_detail_cep/(?P<pk>\d+)/$', detalle_resultado_cep, name='detalle_resultado_cep'),  

    #otros
    url(r'^contacto/$', contacto, name='contacto'),
    url(r'^validar/$', ValidarFichero, name='validar_fichero'),





]