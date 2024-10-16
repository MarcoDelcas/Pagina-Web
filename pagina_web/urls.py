"""
URL configuration for pagina_web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from comparador import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.dashboard_login, name='login'),
    path('index/',views.dashboard_login,name='login'),
    path('home/',views.dashboard_home, name = 'home'),
     path('dashboard_automoviles/',views.dashboard_automoviles, name='dashboard_automoviles'),
    path('dashboard_diagramas/',views.dashboard_diagramas, name='dashboard_diagramas'),
    path('dashboard_vendedores/',views.dashboard_vendedores, name='dashboard_vendedores'),
    path('dashboard_facturas/',views.dashboard_facturas, name='dashboard_facturas'),
    path('dashboard_predictivo/',views.dashboard_predictivo, name='dashboard_predictivo'),
    path('dashboard_comparador/',views.dashboard_comparador, name='dashboard_comparador'),
    path('comparador/',views.dashboard_home, name='comparador'),
]
