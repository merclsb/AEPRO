from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

#para contacto
from django.conf import settings
from django.core.mail import send_mail

#Formualrios Form
from .forms import FormularioContacto

#USUARIO
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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

def contacto(request):
    formulario = FormularioContacto(request.POST or None)

    if formulario.is_valid():
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


    return render (request,plantilla,contexto)






#-----------USUARIO------------

def usuario_nuevo(request):
    if request.method=='POST':
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/')
    else:
        formulario = UserCreationForm()# se puede añadir emial ?
    context = {'formulario': formulario}
    return render(request, 'usuario_nuevo.html', context)

def usuario_login(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/usuario/perfil/')
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return HttpResponseRedirect('/usuario/perfil/')
                else:
                    return render(request, 'noactivo.html')
            else:
                return render(request, 'nousuario.html')
    else:
        formulario = AuthenticationForm()
    context = {'formulario': formulario}
    return render(request, 'login.html', context)

@login_required(login_url='/usuario/login/')
def usuario_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/usuario/login/')
def usuario_perfil(request):
    usuario = request.user
    context = {'usuario': usuario}
    return render(request, 'usuario_perfil.html', context)

