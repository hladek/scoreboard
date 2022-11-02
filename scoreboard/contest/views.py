from django.shortcuts import render
from django.http import Http404
from django.shortcuts import render

from django.db.models import Max
from .models import Competition,Contest,Run,Team
# ...
def competition_board(request, competition_id):
    try:
        competition = Competition.objects.get(pk=competition_id)
        participants = competition.participants.all()
        parti = competition.participants.all().annotate(max_score=Max("run__score"))
        runs = Run.objects.filter(competition_id=competition.id)
        results = Run.objects.values("team").annotate(max_score=Max("score")).filter(competition_id=competition.id)
        #results = Run.objects.raw("SELECT team_id,max('score') FROM runs WHERE competition_id=? GROUP BY team_id",params=(competition_id,));
        #aggregate(points=Max("score")).filter(competition_id=competition.id)
    except Competition.DoesNotExist:
        raise Http404("Competition does not exist")
    return render(request, 'contest/board.html', {'competition': competition,"participants":participants,"runs":runs,"results":parti})

# TODO - select from contest
def contest_competitions(request,contest_id):
    contest = Contest.objects.get(pk=contest_id)
    competitions = contest.competition_set.all()
    teams = contest.team_set.all()
    return render(request,"contest/competitions.html",{"contest":contest,"teams":teams,"competitions":competitions})

def contest_team(request,team_id):
    team = Team.objects.get(pk=team_id)
    competitions = team.competition_set.all().annotate(max_score=Max("run__score"))
    # todo calculate team results for each competition
    return render(request,"contest/teams.html",{"team":team,"competitions":competitions})

def index(request):
    contests = list(Contest.objects.all())
    active_contests = filter(lambda x:x.is_active,contests)
    past_contests = filter(lambda x:not x.is_active,contests)
    return render(request,"contest/index.html",{"active_contests":active_contests,"past_contests":past_contests})
# Create your views here.
from . import views

