from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total', 'lineitem_weight',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'date',
                       'shipping_cost', 'order_total',
                       'grand_total',   'original_cart',
                       'stripe_pid', 'order_weight',
                       )

    fields = ('order_number', 'user_profile', 'date',
              'full_name', 'email', 'phone_number',
              'postcode', 'city', 'street_address1',
              'street_address2', 'county', 'shipping_cost',
              'order_total', 'grand_total', 'original_cart',
              'stripe_pid', 'order_weight',
              )

    list_display = ('order_number', 'user_profile', 'date',
                    'full_name', 'order_total',
                    'shipping_cost', 'grand_total',)

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
