from django.shortcuts import render

from .forms import LoginForm


# Create your views here.
def index(request):
    #form = LoginForm()
    '''if request.POST.get('your_email', '') == '':
        ren = render(request, 'index.html', {"form": form})
    else:
        # if correct load collection. else index with error'''
    ren = render(request, 'collection.html')
    return ren
