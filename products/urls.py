from django.urls import path
from . import views
from .views import ProductListView, CategoryView

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('category/<str:slug>', CategoryView, name='category'),    
]


 