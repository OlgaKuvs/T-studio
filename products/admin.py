from django.contrib import admin
from .models import Product, Category, Review


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


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'product',
        'author',
        'comment',
        'rate',
        'created_at',
        'approved',
    )
    readonly_fields = ('user', 'created_at', 'approved',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
