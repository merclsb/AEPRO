from django.shortcuts import render

#para contacto
from django.conf import settings
from django.core.mail import send_mail

#Formualrios Form
from .forms import FormularioContacto


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