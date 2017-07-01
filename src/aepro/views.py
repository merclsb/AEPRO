from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import transaction, IntegrityError

import subprocess

from .models import (
    ResultadoCEP as CEP,
    ResultadoFDA as FDA,
    Analisis,
    )

from .forms import (
    AnalisisModelForm,
    FormularioContacto, 

    )

#CBV
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse

import os
import json
import plotly.offline as opy
import plotly.graph_objs as go

class LoginRequired(object):
    @method_decorator(login_required)
    def dispatch(self, *args,  **kwargs): #def dispatch(self, request ,*args,  **kwargs):
        return super(LoginRequired, self).dispatch(*args, **kwargs) #.dispatch(request, *args, **kwargs)



# Create your views here.
def inicio(request):
    titulo="Inicio"
    saludo = "Hola"
    if request.user.is_authenticated():
        saludo = "Bienvenido" #%s" %(request.user)
    contexto = {
        "titulo":titulo,
        "saludo":saludo,
    }
    return render(request, 'index.html',contexto)

@login_required(login_url='/accounts/login/')
def analisis_model_form_crear(request):
    titulo = "Analisis ModelForm"
    formulario = AnalisisModelForm(request.POST or None, request.FILES or None)

    if formulario.is_valid():
        for key, valor in formulario.cleaned_data.items(): #python3 iteritems -> iter
            print (key,valor)
            instancia = formulario.save(commit=False)
        print (request.FILES)
        print (request.FILES['file'].name)
        print (request.FILES['file'].content_type)
        valores = formulario.cleaned_data.get("tipo_analisis")
        valor_cep=False
        valor_fda=False
        
        
        try:
            with transaction.atomic():#ATOMICO-------------
                #Guardar el usuario que esta realizacion la peticion
                instancia.user = User.objects.get(id=request.user.id)
                #Guardar el archivo proporcionado por el usuario
                instancia.file = request.FILES['file']

                #Por ultimo guardarmos la instacia analisis
                instancia.save()
                #print (instancia.id_analisis)
            
                for k in valores: #['CEP','FDA']
                    if k == 'CEP':
                        #Si no hay existe ningun control estadistico de procesos indicamos valor 1 id_cep=1
                        if CEP.objects.all().count()==0:
                            print ("if",k)
                            obj_cep,valor_cep = CEP.objects.get_or_create(id_cep=1,analisis_id=instancia.id_analisis) #TypeError: unsupported operand type(s) for +: 'NoneType' and 'int
                        else:
                            #si ya existe algun valor, al ultimo le añadimos +1
                            print ("else",k)
                            obj_cep,valor_cep = CEP.objects.get_or_create(id_cep=CEP.objects.all().last().id_cep+1,analisis_id=instancia.id_analisis)
                    elif k =='FDA':
                        if FDA.objects.all().count()==0:
                            print ("if",k)
                            obj_fda,valor_fda = FDA.objects.get_or_create(id_fda=1,analisis_id=instancia.id_analisis)
                        else:
                            print ("else",k)
                            obj_fda,valor_fda = FDA.objects.get_or_create(id_fda=FDA.objects.all().last().id_fda+1,analisis_id=instancia.id_analisis)

                
                #TASK-->Matlab
                #subprocess.Popen( ('python aepro/task_matlab.py {}').format(instancia.id_analisis),shell=True)

        except Exception as e: 
            print (e)
        return HttpResponseRedirect(reverse('analisis_listcbv'))
        #return HttpResponseRedirect(instancia.get_absolute_url())# para redigir al propio analisis creado

    context = {
        "titulo_form":titulo,
        "form":formulario,
    }
    return render(request, "analisis_create_view.html", context)


class AnalisisListView(LoginRequired,ListView):
    model = Analisis
    template_name= "analisis_list_view.html"
    paginate_by = 5
    # por defecto
    # template : analisis_list.html
    #           object_list, ya muestra una lista de todos los objetos
    #method flowchart: metodos que se puede usar en ListView
    def get_queryset(self, *args,  **kwargs):
        qs = super(AnalisisListView, self).get_queryset(*args, **kwargs).filter(user=self.request.user)
        #print (qs)
        #print (qs.first())
        return (qs)

# class UserListView(ListView):
#     model = User
#     template_name = 'core/user_list.html'  # Default: <app_label>/<model_name>_list.html
#     context_object_name = 'users'  # Default: object_list
#     paginate_by = 10
#     queryset = User.objects.all()  # Default: Model.objects.all()



class AnalisisDetailView(LoginRequired,DetailView):
    model = Analisis
    template_name= "analisis_detail_view.html"#template: object
    #method flowchart: metodos que se puede usar en DetailView
    def get_queryset(self, *args,  **kwargs):
        qs = super(AnalisisDetailView, self).get_queryset(*args, **kwargs).filter(user=self.request.user)
        #print (qs)
        #print (qs.first())
        return (qs)



#guardar como pdf

class AnalisisDeleteView(LoginRequired,DeleteView):
    model = Analisis 
    template_name = 'analisis_delete_view.html'

    #Filtrar los resultados solo para el usuario que realiza la solicitud
    def get_queryset(self, *args,  **kwargs):
        qs = super(AnalisisDeleteView, self).get_queryset(*args, **kwargs).filter(user=self.request.user)
        #print (qs)
        #print (qs.first())
        return (qs)

    def get_success_url(self):
        return reverse('analisis_listcbv')


class AnalisisUpdateView(LoginRequired,UpdateView):#--> models:Analisis:get_absolute_url
    model = Analisis 
    fields = ['titulo_descriptivo','comentario']
    
    template_name = 'analisis_update_view.html'

    #Filtrar los resultados solo para el usuario que realiza la solicitud
    def get_queryset(self, *args,  **kwargs):
        qs = super(AnalisisUpdateView, self).get_queryset(*args, **kwargs).filter(user=self.request.user)
        print (qs)
        print (qs.first())
        return (qs)
        
    def get_success_url(self):
        return reverse('analisis_listcbv')

@login_required(login_url='/accounts/login/')
def detalle_resultado_fda(request, pk):
    pass

@login_required(login_url='/accounts/login/')
def detalle_resultado_cep(request, pk):
    pass



def contacto(request):
    formulario = FormularioContacto(request.POST or None)

    if formulario.is_valid():
        #print (formulario.cleaned_data.get("email"))
        # for i in formulario.cleaned_data:
        #     print (i+":")
        #     print (formulario.cleaned_data.get(i))
        form_email =  formulario.cleaned_data.get("email")
        form_mensaje = formulario.cleaned_data.get("mensaje")
        form_nombre = formulario.cleaned_data.get("nombre")
        email_asunto = 'Email de Contacto'
        email_from = settings.EMAIL_HOST_USER
        email_to = [email_from,"merc303@gmail.com"]
        email_mensaje = " %s: %s enviado por %s" %(form_nombre, form_mensaje, form_email)
        send_mail(
            email_asunto,
            email_mensaje,
            email_from,
            email_to,
            fail_silently=False
            )
    titulo = "contacto"
    contexto = {
        "titulo":titulo,
        "form":formulario,
    }
    plantilla = "aepro_contacto.html"

    #************** return HttpResponseRedirect('/') -> mensaje enviado
    return render (request,plantilla,contexto)


