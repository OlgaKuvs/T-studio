from django.shortcuts import (render,
    redirect, reverse, get_object_or_404,
    HttpResponse)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.db.models.functions import Concat
from django.db.models import Value
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile, UserAddress
from profiles.forms import ProfileForm, AddressForm
from cart.contexts import cart_contents

import stripe
import json


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, ('Sorry, your payment cannot be '
                                 'processed right now. Please try '
                                 'again later.'))
        return HttpResponse(content=e, status=400)
    

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        cart = request.session.get('cart', {})               

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': 'IE',
            'postcode': request.POST['postcode'],
            'city': request.POST['city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        full_name = request.POST['full_name']
        name_parts = full_name.split()
        if len(name_parts) < 2:
            messages.error(request, "Please enter your full name " 
                           "with both first and last names.")
            return redirect(reverse('checkout'))
             
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_cart = json.dumps(cart)
            order.save()
            for item_id, item_data in cart.items():
                try:
                    product = Product.objects.get(id=item_id)                    
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=item_data,
                    )
                    order_line_item.save()                  
                     
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your cart wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_cart'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
            
    else:
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request,
                            "There's nothing in your cart at the moment")
            return redirect(reverse('products:products'))
        
        current_cart = cart_contents(request)
        total = current_cart['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,       
        )
        # Attempt to prefill the form with any info
        # the user maintains in their profile
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                address = UserAddress.objects.filter(
                    username=profile, is_default=True).first()                
                full_name = UserProfile.objects.annotate(full_name=Concat(
                    'first_name', Value(' '), 'last_name')).get(
                    user=request.user).full_name
                if address:
                    order_form = OrderForm(initial={
                        'full_name': full_name, 
                        'email': request.user.email,
                        'phone_number': profile.phone_number,
                        'country': address.profile_country,
                        'postcode': address.profile_postcode,
                        'city': address.profile_city,
                        'street_address1': address.profile_street_address1,
                        'street_address2': address.profile_street_address2,
                        'county': address.profile_county,
                    })
                else:
                    order_form = OrderForm(initial={                        
                        'email': request.user.email,                       
                    })

            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, ('Stripe public key is missing. '
                                  'Did you forget to set it in '
                                  'your environment?'))
        
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,       
    }
    return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)          
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()
               
        # Save the user's info
        if save_info:
            first_name, last_name = order.full_name.split(' ', 1)
            profile_data = {
                'first_name': first_name,
                'last_name': last_name,
                'phone_number': order.phone_number,                
            }
            user_profile_form = ProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()
            
            if not UserAddress.objects.filter(
                username = profile,                              
                profile_street_address1 = order.street_address1,
                profile_street_address2 = order.street_address2,
                profile_city = order.city,
                profile_county = order.county,
                profile_postcode = order.postcode,                
                ).exists():            
            
                address = UserAddress.objects.create(
                    username = profile,                              
                    profile_street_address1 = order.street_address1,
                    profile_street_address2 = order.street_address2,
                    profile_city = order.city,
                    profile_county = order.county,
                    profile_postcode = order.postcode,
                    profile_country = order.country,
                    is_default = False
                )

    messages.success(request, f'Order successfully processed! \
    Your order number is {order_number}. A confirmation \
    email will be sent to {order.email}.')

    # Send confirmation e-mail
    cust_email = order.email
    subject = render_to_string(
        'checkout/confirmation_emails/confirmation_email_subject.txt',
        {'order': order})
    body = render_to_string(
        'checkout/confirmation_emails/confirmation_email_body.txt',
        {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})
    
    email=EmailMessage(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [cust_email],
    )
    email.send(fail_silently=False)
    
    if 'cart' in request.session:
        del request.session['cart']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'save_info': save_info,
    }

    return render(request, template, context)