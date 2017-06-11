# -*- coding: utf-8 -*-
from django import forms
#widget que permite usar datetiempicker en el formulario para seleccion dia y hora
from bootstrap3_datetime.widgets import DateTimePicker
#lib/python3.4/site-packages/bootstrap3_datetime/widgets.py
	#from django.forms.utils import flatatt

from .models import (
	Analisis, 
	)

class AnalisisForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    valor = forms.IntegerField()#required=false
    media = forms.FileField()#es correcto asi??

#Puede usarse en Admin, en vez de Meta: Modelo
class AnalisisModelForm(forms.ModelForm):


	file = forms.FileField(allow_empty_file=True,help_text="Solo se permite subir archivos en formato XLS---")
	
	fecha_inicio = forms.DateTimeField(required=False,widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm","pickSeconds": False,
										"defaultDate": "2017-06-4 10:29",}))
	fecha_paso = forms.DateTimeField(required=False,
		widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm",
										"pickSeconds": False,
										"defaultDate": "2017-06-14 10:29",}))
	fecha_fin = forms.DateTimeField(required=False,
		widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm",
										"pickSeconds": False,
										'locale': 'es',
										"defaultDate": "2017-06-30 10:29",
										}))
	

	class Meta:
		model = Analisis
		fields = [
				"titulo_descriptivo",
				"periodo",
				"tipo_analisis",
				"fecha_inicio",
				"fecha_paso",
				"fecha_fin",
				#"file",
				"comentario",
				

				]
		labels = {
				"titulo_descriptivo": 'Titulo',
				"periodo": 'Seleciona Periodo',
				"tipo_analisis": 'Selecciona el analisis a realizar',
				"comentario": 'Indica un comentario si es necesario',
				"file": 'Archivo'


				}

		widgets = {
			"tipo_analisis": forms.CheckboxSelectMultiple(),
					}

		help_texts = {
			"file": "Solo se permite subir archivos en formato XLS",
			"tipo_analisis": "CEP: permite calcular ...\n AFD: Permite calcular ..." ,

		}

		error_message={
			# 'file': 'Solo se perminte XLS',
		}
	
	#Validar el fichero
	def clean_file(self):
		file = self.files['file']
		if file:
			#print (magic.from_file("file", mime=True))
			print (file)
		return file

	#VALIDAR LAS FECHAS
	def clean(self):
		cleaned_data = super(AnalisisModelForm, self).clean()
		f1 = self.cleaned_data['fecha_inicio']
		f2 = self.cleaned_data['fecha_paso']
		f3 = self.cleaned_data['fecha_fin']
		if not f1 < f2:
			raise forms.ValidationError("La fecha de paso es inferior a la inicio!")
		if not f1 < f3:
			raise forms.ValidationError("La fecha final es inferior a la inicio!")
		if not f2 < f3:
			raise forms.ValidationError("La fecha final es inferior a la de paso!")





class FormularioContacto(forms.Form):
	nombre = forms.CharField(max_length=100)#required=false
	email =  forms.EmailField()
	mensaje = forms.CharField(widget=forms.Textarea)

	def clean_email(self):
		email = self.cleaned_data.get("email")
		#validaciones
		return email




