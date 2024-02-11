from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.functions import Concat
from django.db.models import Value

from .forms import ContactForm
from profiles.models import UserProfile


def contact(request):
    """A view to return contact form and contact us page"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,
                             'Your message has been sent',
                             extra_tags='flag')
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone_number']
            message = form.cleaned_data['message']
            subject = 'New Contact Us Form Submission'
            body = f'''Name: {name}\nEmail: {email}
            Phone:{phone}\nMessage: {message}'''
            # Send e-mail with contact form data to admin
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                ['tstudio.ie@gmail.com'],
                fail_silently=False,
            )
            return redirect(reverse('core'))
        else:
            messages.error(request,
                           'Something went wrong. Please try again.')
    else:
        # Prefill contact form with user's data saved in db
        if request.user.is_authenticated:
            full_name = UserProfile.objects.annotate(full_name=Concat(
                    'first_name', Value(' '), 'last_name')).get(
                    user=request.user).full_name
            user = get_object_or_404(UserProfile, user=request.user)
            form = ContactForm()
            form.fields['email'].initial = request.user.email
            form.fields['name'].initial = full_name
            form.fields['phone_number'].initial = user.phone_number
        else:
            form = ContactForm()

    template = 'contact/contact.html'
    context = {
        'form': form
    }
    return render(request, template, context)
