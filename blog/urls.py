from django.contrib import admin
from django.urls import path, include
from blog import views


app_name ="blog"

urlpatterns=[
    path('', views.index,name='home'),
    path('contact/', views.contact,name='contact'),
    path('about/', views.about,name='about'),
    path('search/', views.search,name='search'),
]