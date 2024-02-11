from django.db import models
from django.core.validators import RegexValidator


class Contact(models.Model):
    """Model for contact form"""
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_regex = RegexValidator(
        regex=r'^(\+\d{1,3})?,?\s?\d{7,15}$',
        message="Please enter a correct phone number. "
                "Up to 15 digits without spaces allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, null=False, blank=False)
    message = models.TextField()

    def __str__(self):
        return f"{self.name}, {self.phone_number}"
