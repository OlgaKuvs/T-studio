from django.shortcuts import render
from .models import Product, Category
from django.views.generic import ListView

class ProductListView(ListView):
    model = Product    
    template_name = 'products/products.html'
    context_object_name = 'products'
    paginate_by = 8
    
    def get_queryset(self):
        queryset = super(ProductListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset
    
    def get_context_data(self, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        context['categories'] = Category.objects.all()        
        return context

