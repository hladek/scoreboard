from django.shortcuts import render
from django.http import Http404
from django.shortcuts import redirect

def index(request):
    return redirect("contest/")


