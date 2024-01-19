from django import forms
from django.forms import ModelForm
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'Name',
            'email': 'Email',
            'phone_number': 'Phone',
            'message': 'Message',           
        }

        self.fields['name'].widget.attrs['autofocus'] = True