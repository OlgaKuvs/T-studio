from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review  
        fields = ('author', 'comment', 'rate')

        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'maxlength': 1000}),
            'rate': forms.RadioSelect(attrs={'class': 'form-control', 'class': 'form-check-inline'}),
        } 