from django.shortcuts import render, redirect, reverse
from .forms import ContactForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def contact(request):
    """A view to return contact form and page"""
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
            \nPhone:{phone}\nMessage: {message}'''
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
        form = ContactForm()

    template = 'contact/contact.html'
    context = {
        'form': form
    }
    return render(request, template, context)

