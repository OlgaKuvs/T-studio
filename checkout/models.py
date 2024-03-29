import uuid
from django.db import models
from django.db.models import Sum
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from products.models import Product
from cart.models import Shipping
from profiles.models import UserProfile, UserAddress


def clean_full_name(value):
    if len(value.split()) < 2:
        raise ValidationError("Please enter your full name")
    return value


class Order(models.Model):

    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='orders')
    full_name = models.CharField(
        validators=[clean_full_name], max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_regex = RegexValidator(
        regex=r'^(\+\d{1,3})?,?\s?\d{7,15}$',
        message="Please enter a correct phone number. "
                "Up to 15 digits without spaces allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, null=False, blank=False)
    country = models.CharField(
        max_length=50, default='IE', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, choices=UserAddress.COUNTIES)
    date = models.DateTimeField(auto_now_add=True)
    shipping_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    original_cart = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default='')
    order_weight = models.IntegerField(null=True, blank=True)

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total and shipping each time a line item is added,
        accounting for delivery costs.
        """
        self.order_total = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0
        self.order_weight = self.lineitems.aggregate(
            Sum('lineitem_weight'))['lineitem_weight__sum'] or 0

        all_rates = Shipping.objects.order_by('order_weight')
        for r in all_rates:
            if r.order_weight > self.order_weight + 100:
                parcel_weight = r.order_weight
                break

        self.shipping_cost = Shipping.objects.filter(
            order_weight=parcel_weight).values_list('postal_rates').first()[0]
        if self.order_total:
            self.grand_total = self.order_total + self.shipping_cost
        else:
            self.grand_total = 0
            self.shipping_cost = 0
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


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
    lineitem_weight = models.IntegerField(null=False, blank=False,
                                          editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.product.price * self.quantity
        self.lineitem_weight = self.product.weight * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
