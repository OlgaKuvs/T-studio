from django.shortcuts import render

# Create your views here.

def index(request):
    """ A view to return the index page """
    return render(request, 'core/index.html')

def thai_massage(request):
    """ A view to return the thai_massage page """
    return render(request, 'core/thai_massage.html')