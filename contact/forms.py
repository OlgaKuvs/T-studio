from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            'message': forms.Textarea(
                attrs={'rows': 5, 'cols': 90, 'maxlength': 500})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'Name',
            'email': 'Email',
            'phone_number': 'Phone',
            'message': 'Message',
        }

        self.fields['name'].widget.attrs['autofocus'] = True
        self.fields['name'].widget.attrs['autocomplete'] = 'name'
        self.fields['email'].widget.attrs['autocomplete'] = 'email'
        self.fields['phone_number'].widget.attrs['autocomplete'] = 'tel'
        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder

