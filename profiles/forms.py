from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from checkout.models import Order
from .models import User, UserProfile, UserAddress


class ProfileForm(forms.ModelForm):
    """User account form to edit base information """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Submit'))        

    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=15)

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'phone_number']


class AddressForm(ModelForm):
    """Address form to change shipping information"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Submit'))
        self.fields['street_address2'].required = False
        self.fields['postcode'].required = False

    profile_street_address1 = forms.CharField(max_length=100)
    profile_street_address2 = forms.CharField(max_length=100)
    profile_city = forms.CharField(max_length=30)
    profile_county = forms.ChoiceField(choices=Order.COUNTIES)
    profile_postcode = forms.CharField(max_length=30)
    profile_country = forms.CharField(max_length=30)

    