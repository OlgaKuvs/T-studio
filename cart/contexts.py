from django.shortcuts import get_object_or_404
from products.models import Product
from .models import Shipping


def cart_contents(request):

    cart_items = []
    total = 0
    product_count = 0
    line_items_weight = 0
    total_weight = 0
    parcel_weight = 0
    cart = request.session.get('cart', {})

    for item_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=item_id)
        total += quantity * product.price
        product_count += quantity
        line_items_weight = quantity * product.weight
        total_weight += line_items_weight
        cart_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })

    """Get the shipping cost from the database for
    the current parcel weight + 100g per packaging """

    all_rates = Shipping.objects.order_by('order_weight')
    for r in all_rates:
        if r.order_weight > total_weight + 100:
            parcel_weight = r.order_weight
            break

    shipping_cost = Shipping.objects.filter(order_weight=parcel_weight)\
        .values_list('postal_rates').first()[0]

    if total:
        grand_total = shipping_cost + total
    else:
        grand_total = 0

    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'grand_total': grand_total,
        'shipping_cost': shipping_cost,
    }
    return context
