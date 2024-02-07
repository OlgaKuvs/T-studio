from django.contrib import admin
from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    """Contact details admin"""
    list_display = ('name',
                    'email',
                    'phone_number',
                    'message')


admin.site.register(Contact, ContactAdmin)
