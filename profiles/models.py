from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    A user profile model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.user.username


class UserAddress(models.Model):

    COUNTIES = [
        ('', 'Choose a county *'),
        ('carlow', 'Carlow'),
        ('cavan', 'Cavan'),
        ('clare', 'Clare'),
        ('cork', 'Cork'),
        ('donegal', 'Donegal'),
        ('dublin', 'Dublin'),
        ('galway', 'Galway'),
        ('kerry', 'Kerry'),
        ('kildare', 'Kildare'),
        ('kilkenny', 'Kilkenny'),
        ('laois', 'Laois'),
        ('leitrim', 'Leitrim'),
        ('limerick', 'Limerick'),
        ('longford', 'Longford'),
        ('louth', 'Louth'),
        ('mayo', 'Mayo'),
        ('meath', 'Meath'),
        ('monaghan', 'Monaghan'),
        ('offaly', 'Offaly'),
        ('roscommon', 'Roscommon'),
        ('sligo', 'Sligo'),
        ('tipperary', 'Tipperary'),
        ('waterford', 'Waterford'),
        ('westmeath', 'Westmeath'),
        ('wexford', 'Wexford'),
        ('wicklow', 'Wicklow')
    ]

    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                 related_name='addresses')
    profile_street_address1 = models.CharField(
        max_length=80, null=True, blank=True)
    profile_street_address2 = models.CharField(
        max_length=80, null=True, blank=True)
    profile_city = models.CharField(max_length=40, null=True, blank=True)
    profile_county = models.CharField(
        max_length=80, choices=COUNTIES, null=True, blank=True)
    profile_postcode = models.CharField(max_length=20, null=True, blank=True)
    profile_country = models.CharField(max_length=50, default='IE')
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return str(self.username)

    class Meta:
        verbose_name_plural = 'User Addresses'


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()
