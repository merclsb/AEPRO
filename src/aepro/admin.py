# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from .models import Analisis
from .forms import AnalisisModelForm

class AdminAnalisis(admin.ModelAdmin):
	list_display=["titulo_descriptivo","timestamp"]
	list_display_links = ["titulo_descriptivo"]
	list_filter = ["timestamp","user"]
	#list_editable = ["email"]
	search_fields=["titulo_descriptivo"]

	class Meta:
		model = Analisis
	#o
	#form = AnalisisModelForm

admin.site.register(Analisis,AdminAnalisis)