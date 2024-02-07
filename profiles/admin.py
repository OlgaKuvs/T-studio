from django.contrib import admin
from .models import UserProfile, UserAddress


class UserProfileAdmin(admin.ModelAdmin):
    """User Profile details admin"""
    list_display = ('user', 'first_name', 'last_name', 'phone_number')


class UserAddressAdmin(admin.ModelAdmin):
    """User Addresses details admin"""
    list_display = ('username',
                    'profile_street_address1',
                    'profile_street_address2',
                    'profile_city',
                    'profile_county',
                    'profile_postcode',
                    'is_default')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserAddress, UserAddressAdmin)
