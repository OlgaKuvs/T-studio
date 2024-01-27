from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='core'),
    path('thai_massage', views.thai_massage, name='thai_massage'),
    path('el_stimulation', views.el_stimulation, name='el_stimulation'), 
    path('mech_therapy', views.mech_therapy, name='mech_therapy'),
    path('yoga_therapy', views.yoga_therapy, name='yoga_therapy'),
    path('baby_massage', views.baby_massage, name='baby_massage'),
    path('massage', views.massage, name='massage'),
    path('j_manipulations', views.j_manipulations, name='j_manipulations'),
    path('yoga', views.yoga, name='yoga'),
]
