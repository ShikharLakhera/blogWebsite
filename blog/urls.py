from django.contrib import admin
from django.urls import path, include
from blog import views


app_name ="blog"

urlpatterns=[
    path('', views.index,name='home'),
    path('contact/', views.contact,name='contact'),
    path('about/', views.about,name='about'),
    path('search/', views.search,name='search'),
    path('signup/', views.handleSignup.as_view(),name='signup'),
    path('login/', views.loginhandle.as_view(),name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('profile/<str:username>/', views.profileView.as_view(),name='profile'),
    path('bioedit/', views.editBio.as_view(),name='editBio'),
    path('usrprofile/<str:author>',views.viewAuthorProfile.as_view(),name='viewAuthor'),
    path('postBlog/',views.postBlog.as_view(),name='postBlog'),
]
