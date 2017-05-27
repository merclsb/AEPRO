# -*- coding: utf-8 -*-
"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^', include('aepro.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),#REGISTRATION REDUX
]
if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#REGISTRATION REDUX
#http://127.0.0.1:8000/accounts/register/

""" 
^accounts/ ^activate/complete/$ [name='registration_activation_complete']
^accounts/ ^activate/(?P<activation_key>\w+)/$ [name='registration_activate']
^accounts/ ^register/complete/$ [name='registration_complete']
^accounts/ ^register/closed/$ [name='registration_disallowed']
^accounts/ ^register/$ [name='registration_register']
^accounts/ ^login/$ [name='auth_login']
^accounts/ ^logout/$ [name='auth_logout']
^accounts/ ^password/change/$ [name='auth_password_change']
^accounts/ ^password/change/done/$ [name='auth_password_change_done']
^accounts/ ^password/reset/$ [name='auth_password_reset']
^accounts/ ^password/reset/complete/$ [name='auth_password_reset_complete']
^accounts/ ^password/reset/done/$ [name='auth_password_reset_done']
^accounts/ ^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$ [name='auth_password_reset_confirm'] 
"""