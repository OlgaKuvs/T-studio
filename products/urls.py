from django.urls import path
from . import views
from .views import ProductListView, CategoryView, ReviewView

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('category/<str:slug>/', CategoryView, name='category'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>', views.delete_product, name='delete_product'),
    path('review_product/<int:product_id>/<int:order_id>/', ReviewView.as_view(), name='review_product'),
    path('show_reviews/', views.show_reviews, name='show_reviews'),
    path('approve_review/<int:product_id>/<int:review_id>/', views.approve_review, name='approve_review'),
]

