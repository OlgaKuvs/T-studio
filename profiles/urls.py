from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [ 
    path('', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('shipping_addresses/', views.shipping_addresses, name='shipping_addresses'),
    path('add_address/', views.add_address, name='add_address'),
    path('delete_address/<int:id>/', views.delete_address, name='delete_address'),
    path('edit_address/<int:id>/', views.edit_address, name='edit_address'),
    path('orders/', views.orders, name='orders'),
    path('order_details/<int:order_id>/', views.order_details, name='order_details'),
]