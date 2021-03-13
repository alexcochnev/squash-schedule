"""schedule URL Configuration

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
from schedule_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.api_index, name='api_index'),
    path('leninka/', views.api_leninka, name='api_leninka'),
    path('leninka_days/', views.api_leninka_days, name='api_leninka_days'),
    path('dubrovka/', views.api_dubrovka, name='api_dubrovka'),
    path('dubrovka_day/', views.api_dubrovka_day, name='api_dubrovka_day'),
    path('shabolovka/', views.api_shabolovka, name='api_shabolovka'),
    path('shabolovka_day/', views.api_shabolovka_day, name='api_shabolovka_day'),
]
