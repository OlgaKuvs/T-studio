from django.contrib import admin
from .models import Shipping

class ShippingAdmin(admin.ModelAdmin):
    list_display = (
        'order_weight',
        'postal_rates',        
    )

admin.site.register(Shipping, ShippingAdmin)

