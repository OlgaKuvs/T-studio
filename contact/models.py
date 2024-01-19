from django.db import models
from django.core.validators import RegexValidator


class Contact(models.Model):
    """Model for contact form"""
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', 
        message="Phone number must be entered in the format:"
                "'+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    message = models.TextField()
    
    def __str__(self):
        return self.name, self.phone_number