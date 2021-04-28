"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,re_path
from django.views.generic.base import RedirectView
from app01 import views

urlpatterns = [

    #re_path('home/', views.home),#新版本中要使用正则表达式只能有re_path,path是不能用正则表达的
    re_path('^home/(\d+)',views.date),
    path('home/',views.home),
    path('index/',views.index),
    path('index/favicon.ico',RedirectView.as_view(url='static/favicon.ico')),
    # path('login/',views.Login.as_view()),
    path('login/',views.Login,name='login'),
    path('mystatic/',views.mystatic),
    path('add/',views.add),
    path('book_show/',views.book_show,name='book_show'),
    path('index/',views.index,name = 'index'),
    path('index2/',views.index2,name='index2'),
    path('index3/',views.index3,name='index3'),
    path('register/',views.register,name='register'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('ajax/',views.ajax,name ='ajax'),
    path('picture/',views.picture,name = 'picture'),
    path('opinion_details/',views.opinion_details,name = 'opinion_details'),
    path('credit/',views.credit,name = 'credit'),
    path('opinion_input/',views.opinion_input,name = 'opinion_input'),
    path('profile/',views.profile,name = 'profile')
]
