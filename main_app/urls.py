from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    #checkout path
    #details path
    #? will the home page also display listing after log-in?
]