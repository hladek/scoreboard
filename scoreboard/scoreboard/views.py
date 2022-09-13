from django.shortcuts import render
from django.http import Http404
from django.shortcuts import render

def index(request):
    return render(request,"scoreboard/index.html")

# Create your views here.
from . import views

