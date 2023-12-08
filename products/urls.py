from django.urls import path
from . import views
from .views import ProductListView

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('category/<int:category_id>', ProductListView.as_view(), name='category'),
    path('page<int:page>/', ProductListView.as_view(), name='paginator'), 
]


 