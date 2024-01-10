from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages

from .models import UserProfile, UserAddress
from checkout.models import Order
from .forms import ProfileForm, AddressForm 


def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)   
    template = 'profiles/profile.html'
    context = {
        'profile': profile,
    }
    return render(request, template, context)


def edit_profile(request):
    """ Edit profile information """
    profile = get_object_or_404(UserProfile, user=request.user)
    form = ProfileForm(instance=profile)
    if request.POST:
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.info(request,                        
                        'Your profile has been updated')
        return redirect('profile')
    form = ProfileForm(instance=profile)
    context = {
        'form': form
    }
    template = 'profiles/edit_profile.html'
    return render(request, template, context)


def shipping_addresses(request):
    """ Display the user's shipping addresses"""
    username = get_object_or_404(UserProfile, user=request.user)      
    addresses = UserAddress.objects.filter(
        username_id=username.id).order_by('-is_default')
    if addresses.exists():
        template = 'profiles/shipping_addresses.html'
    else:
        return redirect('add_address')
    context = {
        'addresses': addresses,        
    }    
    return render(request, template, context)


def add_address(request):
    """ Add new shipping address """
    username = get_object_or_404(UserProfile, user=request.user)   
    all_addresses = UserAddress.objects.filter(username_id=username.id)
    if request.method == 'POST':
        form = AddressForm(request.POST) 
        if form.is_valid():
            """ Check if user wants to save 
            this shipping address as default or
            if user has no addresses yet """ 
            if form.cleaned_data[
                'is_default'] == True or not all_addresses.exists():
                is_default = True               
                for a in all_addresses:
                    a.is_default = False                    
                    a.save()
            else:
                is_default = False 

            address = UserAddress.objects.create(
                username = username,
                profile_street_address1 = form.cleaned_data[
                    'profile_street_address1'],
                profile_street_address2 = form.cleaned_data[
                    'profile_street_address2'],
                profile_city = form.cleaned_data[
                    'profile_city'],
                profile_county = form.cleaned_data[
                    'profile_county'],
                profile_postcode = form.cleaned_data[
                    'profile_postcode'],
                profile_country = 'IE',
                is_default = is_default
            )            
            address.save()            
            messages.info(request, 'Shipping address has been added successfully')
            return redirect('shipping_addresses')
        else:
            messages.error(request, 'Please ensure the form is valid.')
    else:
        form = AddressForm()
        form.fields['profile_country'].initial = 'Ireland'
        template = 'profiles/add_address.html'
        context = {
            'form': form,                 
        }
        return render(request, template, context)
    

def delete_address(request, id):
    """ Delete shipping address """ 
    user = get_object_or_404(UserProfile, user=request.user)
    address = UserAddress.objects.get(id=id, username_id=user.id)
    delete_address = request.GET.get('delete_address')
    if delete_address == 'true':
        address.delete()        
        messages.info(request,
                      "Your address has been deleted.")
        return redirect('shipping_addresses')
    else:
        template = 'profiles/delete_address.html'
        context = {
            'address': address,
            'id': address.id,                   
        }
        return render(request, template, context)
    

def edit_address(request, id):
    """ Edit shipping address """ 
    user = get_object_or_404(UserProfile, user=request.user)      
    address = UserAddress.objects.get(id=id, username_id=user.id)
    all_addresses = UserAddress.objects.filter(username_id=user.id)   
    
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            """ Check if user wants to save 
            this shipping address as default """ 
            if form.cleaned_data[
                'is_default'] == True:
                address.is_default = True               
                for a in all_addresses:
                    a.is_default = False                    
                    a.save()
            else:
                address.is_default = False 
            address.profile_country = 'IE'
            form.save()
            messages.info(request, 'Successfully updated address!')
            return redirect(reverse('shipping_addresses'))
        else:
            messages.error(request,
                           'Failed to update address.'
                           'Please ensure the form is valid.')
    else:
        address.profile_country = 'Ireland'
        form = AddressForm(instance=address)    
        template = 'profiles/edit_address.html'
        context = {
            'form': form,
            'address': address,            
        }
        return render(request, template, context)
    

def orders(request):
    """ Display the user's orders"""
    username = get_object_or_404(UserProfile, user=request.user)      
    orders = Order.objects.filter(
        user_profile_id=username.id).order_by('-date')
    template = 'profiles/orders.html'
    context = {
        'orders': orders,        
    }    
    return render(request, template, context)


def order_details(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    template = 'profiles/order_details.html'
    context = {
        'order': order,        
    }    
    return render(request, template, context)
    
    


    



