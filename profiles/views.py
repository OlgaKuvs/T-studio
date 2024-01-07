from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import UserProfile, UserAddress
from .forms import ProfileForm, AddressForm 


def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)
    form = ProfileForm(instance=profile)
    template = 'profiles/profile.html'
    context = {
        'profile':  profile,
        'form':  form,
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
            user has no addresses yet """    
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
            messages.success(request, 'Shipping address has been added successfully')
            return redirect('profile')
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


def shipping_addresses(request):
    """ Display the user's shipping addresses"""
    username = get_object_or_404(UserProfile, user=request.user)      
    addresses = UserAddress.objects.filter(username_id=username.id)  
    template = 'profiles/shipping_addresses.html'
    context = {
        'addresses': addresses,        
    }    
    return render(request, template, context)
