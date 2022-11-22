from django.shortcuts import render
from django.http import Http404
from django.shortcuts import render

from django.db.models import Max
from .models import Competition,Contest,Run,Team,ItemStates


def get_competition_results(competition):
    return competition.participants.all().annotate(max_score=Max("run__score")).filter(run__competition_id=competition.id)

def frame_board(request,competition_id):
    competition = Competition.objects.get(pk=competition_id)
    parti = get_competition_results(competition)
    return render(request, 'contest/frame_board.html', {"competition":competition,"results":parti})

def frame_runs(request,competition_id):
    competition = Competition.objects.get(pk=competition_id)
    runs = Run.objects.filter(competition_id=competition.id).order_by("-score","team__name","start_time")
    return render(request, 'contest/frame_runs.html', {"runs":runs})

# ...
def competition_board(request, competition_id):
    try:
        # TODO add timer
        competition = Competition.objects.get(pk=competition_id)
        participants = competition.participants.all().order_by("name")
        parti = get_competition_results(competition)
        runs = Run.objects.filter(competition_id=competition.id).order_by("-score","team__name","start_time")
    except Competition.DoesNotExist:
        raise Http404("Competition does not exist")
    return render(request, 'contest/competition_board.html', {"contest":competition.contest,'competition': competition,"participants":participants,"runs":runs,"results":parti})

def contest_competitions(request,contest_id):
    contest = Contest.objects.get(pk=contest_id)
    # TODO sort
    competitions = contest.competition_set.select_related()
    teams = contest.team_set.select_related().all()
    return render(request,"contest/competitions.html",{"contest":contest,"teams":teams,"competitions":competitions})

def frame_competitions(request,contest_id):
    contest = Contest.objects.get(pk=contest_id)
    competitions = contest.competition_set.select_related()
    return render(request,"contest/frame_competitions.html",{"competitions":competitions})

def frame_participants(request,contest_id):
    contest = Contest.objects.get(pk=contest_id)
    teams = contest.team_set.select_related().all()
    return render(request,"contest/frame_participants.html",{"teams":teams})

def contest_team(request,team_id):
    team = Team.objects.get(pk=team_id)
    competitions = team.competition_set.all().annotate(max_score=Max("run__score"))
    #.filter(run__competition_id="competition__id")
    # todo calculate team results for each competition
    return render(request,"contest/teams.html",{"contest":team.contest,"team":team,"competitions":competitions})

def index(request):
    contests = list(Contest.objects.all())
    active_contests = filter(lambda x:x.status == ItemStates.OPEN or x.status == ItemStates.CLOSED,contests)
    past_contests = filter(lambda x:x.status == ItemStates.OLD,contests)
    return render(request,"contest/index.html",{"active_contests":active_contests,"past_contests":past_contests})
# Create your views here.
from . import views

