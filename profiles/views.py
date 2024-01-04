from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from .models import UserProfile, UserAddress
from .forms import ProfileForm, AddressForm 
from django.contrib.auth.models import User


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
    username = get_object_or_404(UserProfile, user=request.user)    
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():            
            address = UserAddress.objects.create(
                username = username,
                profile_street_address1 = form.cleaned_data['profile_street_address1'],
                profile_street_address2 = form.cleaned_data['profile_street_address2'],
                profile_city = form.cleaned_data['profile_city'],
                profile_county = form.cleaned_data['profile_county'],
                profile_postcode = form.cleaned_data['profile_postcode'],
                profile_country = 'IE'
            )            
            address.save()
            return HttpResponseRedirect(reverse('profile'))
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
