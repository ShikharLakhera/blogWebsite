from django.contrib import admin
from django.urls import path, include
from blogHome import views

app_name='blogHome'

urlpatterns =[
    path('addcoments/<int:post_id>/',views.commentHandler,name='addComments'),
    path('editblog/<slug:slug>',views.editView.as_view(),name='editView'),
    path('',views.blogHome,name='blogHome'),
    path('<slug:slug>/',views.blogPage,name='blogPage'),
]