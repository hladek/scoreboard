from django.shortcuts import render
from django.http import Http404
from django.shortcuts import render

from django.db.models import Max
from .models import Competition,Run
# ...
def board(request, competition_id):
    try:
        competition = Competition.objects.get(pk=competition_id)
        participants = competition.participants.all()
        runs = Run.objects.filter(competition_id=competition.id)
        results = Run.objects.values("team").annotate(max_score=Max("score")).filter(competition_id=competition.id)
        #results = Run.objects.raw("SELECT team_id,max('score') FROM runs WHERE competition_id=? GROUP BY team_id",params=(competition_id,));
        #aggregate(points=Max("score")).filter(competition_id=competition.id)
    except Competition.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'contest/board.html', {'competition': competition,"participants":participants,"runs":runs,"results":results})

def index(request):
    competitions = Competition.objects.all()
    return render(request,"contest/competitions.html",{"competitions":competitions})

# Create your views here.
from . import views

