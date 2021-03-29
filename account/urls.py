from django.contrib import admin
from django.urls import path, include
from . import views

app_name='account'
urlpatterns = [
    path('', views.login, name="login"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout, name="logout"),
]