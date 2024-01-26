from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='core'),
    path('thai_massage', views.thai_massage, name='thai_massage'),
    path('el_stimulation', views.el_stimulation, name='el_stimulation'), 
    path('mech_therapy', views.mech_therapy, name='mech_therapy'),
]
