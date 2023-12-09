from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from django.views.generic import ListView
from django.db.models import Q
from django.contrib import messages


class ProductListView(ListView):
    """A Class Based View to show all products, including search queries"""
    model = Product    
    template_name = 'products/products.html'
    context_object_name = 'products'   
    
    def get_queryset(self):
        queryset = super(ProductListView, self).get_queryset()
        # category_id = self.kwargs.get('category_id')
        # if category_id:
        #     queryset = queryset.filter(category_id=category_id)           
        q = self.request.GET.get('q') 
        if q:
            queryset = self.model.objects.filter(
                Q(name__icontains=q) | Q(description__icontains=q)
                )                    
        return queryset
        
    def get_context_data(self, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        context['categories'] = Category.objects.all()
        # context['category_id'] = self.kwargs.get('category_id')        
        context['q'] = self.request.GET.get('q')                               
        return context

  
def CategoryView(request, slug):
    try:
        current_category = Category.objects.get(name=slug)
        category_products = Product.objects.filter(category=current_category)
        all_categories = Category.objects.all()
        context = {
        'category_products': category_products,
        'slug': slug,
        'categories': all_categories
        }
        return render(request, 'products/products.html', context)
    except:
        messages.error(request, "That category doesn't exist")
        return redirect('products:products')  

