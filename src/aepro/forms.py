# -*- coding: utf-8 -*-
from django import forms

class FormularioContacto(forms.Form):
	nombre = forms.CharField(max_length=100)#required=false
	email =  forms.EmailField()
	mensaje = forms.CharField(widget=forms.Textarea)

	def clean_email(self):
		email = self.cleaned_data.get("email")
		#validaciones
		return email