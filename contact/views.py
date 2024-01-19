from django.shortcuts import render, redirect, reverse
from .forms import ContactForm
from django.contrib import messages

def contact(request):
    """A view to return contact form and page"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 
                            'Your message has been sent',
                            extra_tags='flag')
            return redirect(reverse('core'))
        else:
            messages.error(request,
                           'Something went wrong. Please try again later')
    else:
        form = ContactForm()

    template = 'contact/contact.html'
    context = {
        'form': form
    }
    return render(request, template, context)

