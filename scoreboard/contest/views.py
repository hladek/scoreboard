from django.shortcuts import render
from django.http import Http404
from django.shortcuts import render

from .models import Competition
# ...
def board(request, competition_id):
    try:
        competition = Competition.objects.get(pk=competition_id)
    except Competition.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'contest/board.html', {'competition': competition})

def index(request):
    competitions = Competition.objects.all()
    return render(request,"contest/competitions.html",{"competitions":competitions})

# Create your views here.
from . import views

