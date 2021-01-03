"""myDots URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from myDots import views

urlpatterns = [
    path('', views.home, name='home'),
    url(r'^validate_minimax/$', views.validate_minimax, name='validate_minimax'),
    url(r'^set_dubina/$', views.set_dubina, name='set_dubina'),
    url(r'^set_human/$', views.set_human, name='set_human'),
    url(r'^set_comp3/$', views.set_comp3, name='set_comp3'),
    url(r'^set_comp2/$', views.set_comp2, name='set_comp2'),
    url(r'^set_comp/$', views.set_comp, name='set_comp'),
    url(r'^validate_minimaxHard/$', views.validate_minimaxHard, name='validate_minimaxHard'),
    url(r'^validate_minimaxMedium/$', views.validate_minimaxMedium, name='validate_minimaxMedium'),
    path('admin/', admin.site.urls),
    
]
