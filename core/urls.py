from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='core'),
    path('thai_massage', views.thai_massage, name='thai_massage'),
    path('ed_stimulation', views.ed_stimulation, name='ed_stimulation'), 
]
