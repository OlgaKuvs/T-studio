from django.urls import path
from . import views


urlpatterns = [ 
    path('', views.profile, name='profile'),
    path('shipping/', views.shipping_addresses, name='shipping_addresses'),
    path('add_address/', views.add_address, name='add_address'),
]