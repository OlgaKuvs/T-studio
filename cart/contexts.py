from decimal import Decimal

def cart_contents(request):

    cart_items = []
    total = 10
    weight_total = 0
    product_count = 0
    cart = request.session.get('cart', {})
    
    delivery = total * Decimal()
    grand_total = delivery + total

    print(grand_total)
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'weight_total': weight_total,
        'grand_total': grand_total,       
    }

    return context