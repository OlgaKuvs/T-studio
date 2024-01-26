from django.shortcuts import render

# Create your views here.

def index(request):
    """ A view to return the index page """
    return render(request, 'core/index.html')


def thai_massage(request):
    """ A view to return the thai_massage page """
    return render(request, 'core/thai_massage.html')


def el_stimulation(request):
    """ A view to return the electro dinamical stimulation page """
    return render(request, 'core/el_stimulation.html')


def mech_therapy(request):
    """ A view to return the mechanical stimulation page """
    return render(request, 'core/mech_therapy.html')


def yoga_therapy(request):
    """ A view to return the yoga therapy page """
    return render(request, 'core/yoga_therapy.html')