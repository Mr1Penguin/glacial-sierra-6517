from django.shortcuts import render

from .forms import LoginForm

# Create your views here.
def index(request):
	form = LoginForm()
	return render(request, 'index.html', {"form" : form})