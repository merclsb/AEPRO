# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import (
	inicio,
	contacto,
	usuario_nuevo,
	usuario_login,
	usuario_logout,
	usuario_perfil,
	)

urlpatterns = [
    url(r'^$', inicio, name='inicio'),
    #usuario
    url(r'^usuario/nuevo/$', usuario_nuevo, name='usuario_nuevo'),
    url(r'^usuario/login/$', usuario_login, name='usuario_login'),
    url(r'^usuario/logout/$', usuario_logout, name='usuario_logout'),
    url(r'^usuario/perfil/$', usuario_perfil, name='usuario_perfil'),
    #otros
    url(r'^contacto/$', contacto, name='contacto'),
]