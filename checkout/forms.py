from django import forms
from django.core.exceptions import ValidationError

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'city', 'postcode', 'country',
                  'county',)
        
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')           
        name_parts = full_name.split()
        if len(name_parts) < 2:
            raise ValidationError("Please enter your full name")
        return full_name   


    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postcode': 'Postal Code',
            'city': 'City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',
            'country': 'Country',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:           
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]                                   
                self.fields[field].widget.attrs['placeholder'] = placeholder
        self.fields['country'].widget = forms.HiddenInput()
        self.fields[field].widget.attrs['class'] = 'stripe-style-input'
        self.fields[field].label = False