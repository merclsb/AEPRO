# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from multiselectfield import MultiSelectField

from jsonfield import JSONField
#from django.contrib.postgres.fields import JSONField

PERIODOS = (
	('DIA','Dia'),
	('MES','Mes'),
	('AÑO','Año'),
	)
OPERACIONES = (
	('CEP','Control Estadistico de Procesos'),
	('FDA','Analisis Funcional de Datos'),
	)

class Analisis(models.Model):

	#id : autogenerado
	id_analisis = models.AutoField(primary_key=True) #PK = blank=False null=false unique=True
	user = models.ForeignKey(User, on_delete=models.CASCADE) #on_delete=models.CASCADE unique=True
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	titulo_descriptivo = models.CharField(max_length=100)#blank=True, null=True
	periodo= models.CharField(max_length=3, choices=PERIODOS, default=None)
	fecha_inicio = models.DateTimeField()
	fecha_paso = models.DateTimeField()
	fecha_fin = models.DateTimeField()
	file = models.FileField(upload_to='datos_xls/', blank=True, null=True)#upload_to=settings.XML_ROOT upload_to='uploads/%m-%Y/' storage=OverwriteStorage()
	tipo_analisis = MultiSelectField(choices=OPERACIONES,default='CEP')
	comentario = models.TextField(default="Escribe aqui tu comentario",max_length=150)
	

	class Meta:
		ordering = ["-timestamp"]#ordenar los resultados en orden inverso
		verbose_name = "Datos Analisis"
		verbose_name_plural = "Analisis"

	def __str__(self): #Python_3
	 	return '%s,%s,%s' %(str(self.id_analisis), str(self.titulo_descriptivo),str(self.tipo_analisis))


	def __unicode__(self): #Python_2
		return '%s,%s,%s' %(str(self.id_analisis), str(self.titulo_descriptivo),str(self.tipo_analisis))

	def get_absolute_url(self):
		view_name = "analisis_detailcbv"
		return reverse(view_name, kwargs={"pk": self.id_analisis})
		#Para poder acceder a AnalisisDetailView desde el template de AnalisisListView (analisis_lista.html)
		#<li><a href="{{ obj.get_absolute_url}}">{{obj}}</a></li>


class ResultadoCEP(models.Model):
	id_cep = models.AutoField(primary_key=True)
	estado=models.BooleanField(default=False)
	analisis = models.OneToOneField(Analisis ,related_name='analisis_cep',null=True, blank=True, on_delete=models.CASCADE)
	resultados = JSONField(default={})
	pid = JSONField(default={"pid:'',estado:'' "})

	def __str__(self): #Python_3
	 	return '%s,%s,%s' %(str(self.id_cep), str(self.estado),str(self.analisis))

	def get_absolute_url(self):
		view_name = "detalle_resultado_cep"
		return reverse(view_name, kwargs={"pk": self.id_cep})
 

class ResultadoFDA(models.Model):
	id_fda = models.AutoField(primary_key=True)
	#variable que se usa en la vista para indicar si el analisis esta: calculando:False y finalizado:True
	estado=models.BooleanField(default=False)
	analisis = models.OneToOneField(Analisis ,related_name='analisis_fda',null=True, blank=True, on_delete=models.CASCADE)
	resultados = JSONField(default={})
	pid = JSONField(default={"pid:'',estado:'' "})

	def __str__(self): #Python_3
	 	return '%s,%s,%s' %(str(self.id_fda), str(self.estado),str(self.analisis))

	def get_absolute_url(self):
		view_name = "detalle_resultado_fda"
		return reverse(view_name, kwargs={"pk": self.id_fda})
