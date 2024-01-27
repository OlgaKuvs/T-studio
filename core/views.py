from django.shortcuts import render

# Create your views here.

def index(request):
    """ A view to return the index page """
    return render(request, 'core/index.html')


def thai_massage(request):
    """ A view to return the thai massage page """
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


def baby_massage(request):
    """ A view to return the baby massage page """
    return render(request, 'core/baby_massage.html')


def massage(request):
    """ A view to return the classic massage page """
    return render(request, 'core/massage.html')


def j_manipulations(request):
    """ A view to return the joint manipulations page """
    return render(request, 'core/j_manipulations.html')


def yoga(request):
    """ A view to return the yoga page """
    return render(request, 'core/yoga.html')