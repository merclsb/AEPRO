# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import (
	inicio,
	contacto,
	)

urlpatterns = [
    url(r'^$', inicio, name='inicio'),
    url(r'^contacto/$', contacto, name='contacto'),
]