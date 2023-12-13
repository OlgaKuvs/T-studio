from django.db import models
from products.models import Product


class Order(models.Model):
     
    COUNTIES = [
    ('carlow', 'Carlow'),
    ('cavan', 'Cavan'),
    ('clare', 'Clare'),
    ('cork', 'Cork'),
    ('donegal', 'Donegal'),
    ('dublin', 'Dublin'),
    ('galway', 'Galway'),
    ('kerry', 'Kerry'),
    ('kildare', 'Kildare'),
    ('kilkenny', 'Kilkenny'),
    ('laois', 'Laois'),
    ('leitrim', 'Leitrim'),
    ('limerick', 'Limerick'),
    ('longford', 'Longford'),
    ('louth', 'Louth'),
    ('mayo', 'Mayo'),
    ('meath', 'Meath'),
    ('monaghan', 'Monaghan'),
    ('offaly', 'Offaly'),
    ('roscommon', 'Roscommon'),
    ('sligo', 'Sligo'),
    ('tipperary', 'Tipperary'),
    ('waterford', 'Waterford'),
    ('westmeath', 'Westmeath'),
    ('wexford', 'Wexford'),
    ('wicklow', 'Wicklow')
    ]
     
    order_number = models.CharField(max_length=32, null=False, editable=False)    
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(default='Ireland', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, choices=COUNTIES)
    date = models.DateTimeField(auto_now_add=True)
    shipping_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')
    weight = models.IntegerField(null=True, blank=True)


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False,
                              on_delete=models.CASCADE,
                              related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False,
                                on_delete=models.CASCADE)    
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2,
                                         null=False, blank=False,
                                         editable=False)
