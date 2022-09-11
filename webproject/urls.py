"""webproject URL Configuration

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
from django.urls.conf import include
from numpy.lib.npyio import save
from . import view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',view.home,name="home"),
    
    path('house/',view.house, name="house"),
    path('getHouse/', view.getHouse, name="getHouse"),
    path('house/houseOut/', view.houseOut, name="houseOut"),

    path('bank/', view.bank, name="bank"),
    path('getBank/', view.getBank, name="getBank"),
    path('bank/bankOut/', view.bankOut, name="bankOut"),

    path('fraud/', view.fraud, name="class"),
    path('getFraud/', view.getFraud, name="fraud fields"),
    path('fraud/fraudOut/', view.fraudOut, name="fraud output"),

    path('toxic/', view.toxic, name="class"),
    path('getToxic/', view.getToxic, name="toxic fields"),
    path('toxic/toxicOut/', view.toxicOut, name="toxic output")
]
