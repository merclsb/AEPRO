from django.shortcuts import redirect, render, get_object_or_404
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
    UpdateResultadoFDA,
    ValidacionFicheroForm,
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

from subprocess import check_output

def get_pid(name):
    return list(map(int,check_output(["pidof",name]).split()))


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
                subprocess.Popen( ('python aepro/task_matlab.py {}').format(instancia.id_analisis),shell=True)

        except Exception as e: 
            print (e)
        return render(request,'analisis_done.html')
        #return HttpResponseRedirect(instancia.get_absolute_url())# para redigir al propio analisis creado

    context = {
        "titulo_form":titulo,
        "form":formulario,
    }
    return render(request, "analisis_create_view.html", context)


class AnalisisListView(LoginRequired,ListView):
    model = Analisis
    template_name= "analisis_list_view.html"
    paginate_by = 10
    # por defecto
    # template : analisis_list.html
    #           object_list, ya muestra una lista de todos los objetos
    #method flowchart: metodos que se puede usar en ListView
    def get_queryset(self, *args,  **kwargs):
        qs = super(AnalisisListView, self).get_queryset(*args, **kwargs).filter(user=self.request.user)
        #print (qs)
        #print (qs.first())
        return (qs)

    def get_context_data(self, **kwargs):
         context = super(AnalisisListView, self).get_context_data(**kwargs)
         
         context['procesos_activos'] = get_pid("MATLAB")
         return context

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



class AnalisisDeleteView(LoginRequired,DeleteView):
    model = Analisis 
    template_name = 'analisis_delete_view.html'

    #Filtrar los resultados solo para el usuario que realiza la solicitud
    def get_queryset(self, *args,  **kwargs):
        qs = super(AnalisisDeleteView, self).get_queryset(*args, **kwargs).filter(user=self.request.user)
        return (qs)

    def get_success_url(self):
        return reverse('analisis_listcbv')

class AnalisisDeleteViewError(LoginRequired,DeleteView):
    model = Analisis 
    template_name = 'analisis_delete_view_error.html'

    #Filtrar los resultados solo para el usuario que realiza la solicitud
    def get_queryset(self, *args,  **kwargs):
        qs = super(AnalisisDeleteViewError, self).get_queryset(*args, **kwargs).filter(user=self.request.user)
        print(self.request.POST.get('pk'))
        return (qs)
    def get_success_url(self):
        return reverse('analisis_listcbv')



# class AnalisisUpdateView(LoginRequired,UpdateView):#--> models:Analisis:get_absolute_url
#     model = Analisis 
#     fields = ['titulo_descriptivo','comentario']
    
#     template_name = 'analisis_update_view.html'

#     #Filtrar los resultados solo para el usuario que realiza la solicitud
#     def get_queryset(self, *args,  **kwargs):
#         qs = super(AnalisisUpdateView, self).get_queryset(*args, **kwargs).filter(user=self.request.user)
#         print (qs)
#         print (qs.first())
#         return (qs)
        
    # def get_success_url(self):
    #     return reverse('analisis_listcbv')


class Analisis_FDA_UpdateView(LoginRequired,UpdateView):#--> models:Analisis:get_absolute_url
    model = Analisis
    form_class = UpdateResultadoFDA,
    #fields = ['titulo_descriptivo','comentario']
    
    template_name = 'analisis_update_view.html'

    #Filtrar los resultados solo para el usuario que realiza la solicitud
    def get_queryset(self, *args,  **kwargs):
        qs = super(Analisis_FDA_UpdateView, self).get_queryset(*args, **kwargs).filter(user=self.request.user)
        #print(self.kwargs.get('pk',0))
        return (qs)

    def get(self, request,  *args, **kwargs):
        self.object = Analisis.objects.get(id_analisis=kwargs['pk'])
        print("-----")
        print(self.object)
        id_analisis = kwargs['pk']
        analisis = self.model.objects.get(id_analisis=id_analisis)
        f=analisis.analisis_fda.id_fda
        
        form_class = self.get_form_class()
        form = UpdateResultadoFDA(initial={'titulo_descriptivo':analisis.titulo_descriptivo,
                                  'comentario':analisis.comentario,
                                  'nombre_grafica':analisis.analisis_fda.resultados['nombre_grafica'],
                                  'xasix':analisis.analisis_fda.resultados['xasix'],
                                  'yasix':analisis.analisis_fda.resultados['yasix'],
                                  })
        
        context = self.get_context_data(object=self.object, form=form)
        context['xasix'] = analisis.analisis_fda.resultados['xasix'] #whatever you would like
         
        return self.render_to_response(context)


    def get_context_data(self, **kwargs):
         context = super(Analisis_FDA_UpdateView, self).get_context_data(**kwargs)
         return context

    def post (self, request, *args, **kwargs):
        self.object = self.get_object
        id_analisis = kwargs['pk']
        analisis = self.model.objects.get(id_analisis=id_analisis)
        #res_fda = FDA.objects.get(analisis_id=id_analisis)
        print(analisis.analisis_fda.id_fda)
        print("POST")
        #recoger la informacion del formulario
        #Para analisis guardamos el titulo y el comentario
        formulario = self.form_class(request.POST, instance=analisis) # sino se indica la instancia, generaria uno nuevo
        if formulario.is_valid():
          datos_formulario = formulario.cleaned_data
          print(datos_formulario.get('comentario'))
          #formulario['xasix']=analisis.analisis_fda.resultados['xasix']

          nombre_grafica=datos_formulario.get("nombre_grafica")
          xasix=datos_formulario.get("xasix")
          yasix=datos_formulario.get("yasix")
 
          print(yasix)
          #Para el resultado fda guardamos los ejes y el titulo de la grafica
          
          #analisis.analisis_fda.resultados['xasix']
          valores = {
                  "x":analisis.analisis_fda.resultados['x'],
                  "y":analisis.analisis_fda.resultados['y'],
                  "nombre_grafica":nombre_grafica,
                  "xasix":xasix,
                  "yasix":yasix,

          }
          FDA.objects.filter(analisis=id_analisis).update(resultados=valores)
          #print (ResultadoFDA.objects.filter(analisis=sys.argv[1]).update(estado=True))
          print(analisis.analisis_fda.resultados['y'])
          print(analisis.analisis_fda.resultados['xasix'])
          print(analisis.analisis_fda.resultados['yasix'])
          formulario.save()
          return HttpResponseRedirect(self.get_success_url())
        else:
          return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, **kwargs):
      print(self.kwargs['pk'])
      return reverse('detalle_resultado_fda', args=(self.kwargs['pk'],))
      #return reverse('detalle_resultado_fda', args=(self.object.id_analisis,))
    


class Analisis_CEP_UpdateView(LoginRequired,UpdateView):#--> models:Analisis:get_absolute_url
    model = Analisis 
    fields = ['titulo_descriptivo','comentario']
    
    template_name = 'analisis_update_view.html'

    #Filtrar los resultados solo para el usuario que realiza la solicitud
    def get_queryset(self, *args,  **kwargs):
        qs = super(Analisis_CEP_UpdateView, self).get_queryset(*args, **kwargs).filter(user=self.request.user)
        return (qs)
        
    def get_success_url(self, **kwargs):
      return reverse('detalle_resultado_cep', args=(self.object.id_analisis,))
      print(self.object)






@login_required(login_url='/accounts/login/')
def detalle_resultado_fda(request, pk):
    # Controlar que cada usuario solo puede ver sus resultados
    titulo="Resultado del Analisis Funcional de Datos"
    a=Analisis.objects.filter(user_id=request.user.id)
    template = "analisis_resultado_detail_fda.html"
    resultado = get_object_or_404(a, pk=pk)
    periodo=resultado.periodo


    #GRAFICA 1 - LINEA
    out=[]
    trace_r=[]
    trace_out=[]
    data = []

    x = resultado.analisis_fda.resultados['x']
    y = resultado.analisis_fda.resultados['y']
     


    for i in range(len(x)):
        trace_r.append(go.Scatter(y=x[i], marker={'color': 'grey', 'symbol': 104, 'size': "5"},
                        mode="lines",  name= periodo+' :'+str(i+1)))
    for j in range(len(y)):
        #print(j)
        trace_out.append (go.Scatter(y=x[y[j]-1], marker={'color': 'red', 'symbol': 104, 'size': "10"},
                            mode="lines",  name='Outlier ->: '+periodo+' :'+str(y[j]) ) )

    for i in range(len(trace_r)):
        data.append(trace_r[i])

    for j in range(len(trace_out)):
        data.append(trace_out[j])

    data2=go.Data(data)
    layout2=go.Layout(title=resultado.analisis_fda.resultados['nombre_grafica'], xaxis={'title':resultado.analisis_fda.resultados['xasix']}, yaxis={'title':resultado.analisis_fda.resultados['yasix']})
    figure2=go.Figure(data=data2,layout=layout2)
    div2 = opy.plot(figure2, auto_open=False, output_type='div')


    contexto = {
        "titulo":titulo,
        "resultado_form":resultado,
        "resultado_id":pk,
        #'graph':div,
        'graph2':div2,



    }
    return render(request, template, contexto)


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

@login_required(login_url='/accounts/login/')
def ValidarFichero(request):
  estado = ''
  if request.method == 'POST':
    formulario = ValidacionFicheroForm(request.POST or None, request.FILES or None)
    
    if formulario.is_valid():

      estado = 'Formato correcto'
      print (request.FILES)
      print (request.FILES['file'].name)
      print (request.FILES['file'].content_type)
      #formulario.save()
      #return HttpResponseRedirect('/')
  else:
        formulario = ValidacionFicheroForm()

  titulo = "Validar Fichero"
  contexto = {
        "estado":estado,
        "titulo":titulo,
        "form":formulario,
    }
  plantilla = "validar_file.html"
  return render (request,plantilla,contexto)

