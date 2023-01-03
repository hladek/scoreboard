from django.shortcuts import render
from django.http import Http404
from django.shortcuts import render

from django.db.models import Max
from .models import Competition,Contest,Run,Team,ItemStates,Result
import collections



# ...
def competition_board(request, competition_id):
    try:
        # TODO add timer
        competition = Competition.objects.get(pk=competition_id)
        results = Result.objects.filter(competition_id=competition_id).order_by("score").select_related()
        preliminary_results = competition.runs.all().annotate(max_score=Max("run__score")).filter(id=competition_id)
        runs = Run.objects.filter(competition_id=competition.id).order_by("-score","team__name","start_time")
    except Competition.DoesNotExist:
        raise Http404("Competition does not exist")
    return render(request, 'contest/competition_board.html', {"contest":competition.contest,'competition': competition,"runs":runs,"preliminary_results":preliminary_results,"results":results})

def contest_competitions(request,contest_id):
    contest = Contest.objects.get(pk=contest_id)
    # TODO sort
    competitions = Competition.objects.filter(contest_id=contest_id)
    teams = Team.objects.filter(contest_id=contest_id)
    #team_table = []
    over = []
    i2t = {}
    i2c = {}
    over = collections.defaultdict(dict)
    for team in teams:
        for result in team.result_set.all():
            over[team.id][result.competition.id] = result 
    over2 = []
    for team in teams:
        line = []
        for competition in competitions: 
            if competition.id in over[team.id]:
                line.append(over[team.id][competition.id])
            else:
                line.append(None)
        over2.append({"team":team,"results":line})
    print(over2)
    return render(request,"contest/competitions.html",{"contest":contest,"teams":teams,"competitions":competitions,"over":over2})


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

