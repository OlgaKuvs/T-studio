from django import forms
from crispy_forms.helper import FormHelper
from .models import UserProfile, UserAddress


class ProfileForm(forms.ModelForm):
    """User account form to edit base information """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=15)

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'phone_number']


class AddressForm(forms.ModelForm):
    """Address form to change shipping information"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['profile_street_address1'].required = True
        self.fields['profile_city'].required = True
        self.fields['profile_county'].required = True

        placeholders = {
                'profile_street_address1': 'Street Address Line 1',
                'profile_street_address2': 'Street Address Line 2',
                'profile_city': 'City',
                'profile_postcode': 'Postcode',
                'profile_country': 'Ireland',
                'is_default': 'Set as default address',
            }

        self.fields['profile_country'].widget.attrs['disabled'] = True
        for field in self.fields:
            if field != 'profile_county':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False
        self.fields['is_default'].label = 'Set as default address'

    class Meta:
        model = UserAddress
        exclude = ('user',)
        fields = ['profile_street_address1', 'profile_street_address2',
                  'profile_city', 'profile_county',
                  'profile_postcode', 'profile_country',
                  'is_default']
