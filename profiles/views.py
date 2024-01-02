from django.shortcuts import render, get_object_or_404

from .models import UserProfile
from django.contrib.auth.models import User


def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(User, username=request.user.username)
    template = 'profiles/profile.html'
    context = {
        'profile':  profile,
    }

    return render(request, template, context)