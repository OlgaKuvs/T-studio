from django.urls import path
from . import views


urlpatterns = [ 
    path('', views.profile, name='profile'),
    path('shipping_addresses/', views.shipping_addresses, name='shipping_addresses'),
    path('add_address/', views.add_address, name='add_address'),
    path('delete_address/<int:id>/', views.delete_address, name='delete_address'),
]