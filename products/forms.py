from django import forms
from .models import Review, Product, Category
from .widgets import CustomClearableFileInput


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ('rating',)

        widgets = {
            'price': forms.NumberInput(attrs={'min': 1, 'max': 1000}),
            'discount': forms.NumberInput(attrs={'min': 1, 'max': 100}),
            'weight': forms.NumberInput(attrs={'min': 1, 'max': 10000}),
            'stock': forms.NumberInput(attrs={'min': 0, 'max': 10000}),
        }

    image = forms.ImageField(label='Image', required=False,
                             widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['weight'].required = True
        self.fields['category'].choices = friendly_names


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('author', 'comment', 'rate')

        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control',
                                             'maxlength': 1000}),
            'rate': forms.RadioSelect(attrs={'class': 'form-check-inline'}),
        }
