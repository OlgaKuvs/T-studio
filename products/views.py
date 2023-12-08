from django.shortcuts import render
from .models import Product, Category
from django.views.generic import ListView
from django.db.models import Q

class ProductListView(ListView):
    model = Product    
    template_name = 'products/products.html'
    context_object_name = 'products'
   
    
    def get_queryset(self):
        queryset = super(ProductListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        q = self.request.GET.get('q') 
        if q:
            queryset = self.model.objects.filter(
                Q(name__icontains=q) | Q(description__icontains=q)
                )                    
        return queryset
        
    def get_context_data(self, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['q'] = self.request.GET.get('q')                               
        return context

