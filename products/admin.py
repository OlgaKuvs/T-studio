from django.contrib import admin
from .models import Product, Category

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'discount',
        'stock',
        'in_stock',
        'rating',
        'image',
        'weight',
    )

    ordering = ('sku',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',        
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
