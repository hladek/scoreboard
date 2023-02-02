from django.shortcuts import render
from django.http import Http404
from django.shortcuts import render
from django.core.exceptions import PermissionDenied, ValidationError,BadRequest

from django.db.models import Max
from .models import Competition,Contest,Run,Team,ItemStates,Result
import collections
import json


# ...
def competition_board(request, competition_id):
    try:
        competition = Competition.objects.get(pk=competition_id)
        results = Result.objects.filter(competition_id=competition_id).order_by("score").select_related()
        pr = Run.objects.values("team_id").annotate(max_score=Max("score")).filter(competition_id=competition_id)
        preliminary_results = []
        for r in pr:
            tn = Team.objects.get(id=r["team_id"])
            preliminary_results.append({"team_id":r["team_id"],"team_name":tn.name,"max_score":r["max_score"]})

        runs = Run.objects.filter(competition_id=competition.id).order_by("-score","team__name","start_time")
    except Competition.DoesNotExist:
        raise Http404("Competition does not exist")
    return render(request, 'contest/competition_board.html', {"contest":competition.contest,'competition': competition,"runs":runs,"preliminary_results":preliminary_results,"results":results})

def contest_competitions(request,contest_id):
    contest = Contest.objects.get(pk=contest_id)
    # TODO sort
    competitions = Competition.objects.filter(contest_id=contest_id,status__in=["OPEN","CLOSED"])
    teams = Team.objects.filter(contest_id=contest_id)
    #team_table = []
    over = []
    i2t = {}
    i2c = {}
    over = collections.defaultdict(dict)
    # results of teams in competitions
    for team in teams:
        for result in team.result_set.all():
            over[team.id][result.competition.id] = result.score

    # get preliminary results - best runs for each team and each running competition
    running = collections.defaultdict(dict)
    for competition in competitions: 
        if competition.status != "OPEN":
            continue
        pr = Run.objects.values("team_id").annotate(max_score=Max("score")).filter(competition_id=competition.id)
        for r in pr:
            running[r["team_id"]][competition.id] = r["max_score"]
    # transform matrix into table
    table = []
    # one row for each team
    for team in teams:
        line = []
        # one column for each competition
        for competition in competitions: 
            # Final results from judges
            if competition.id in over[team.id] and competition.status == "CLOSED":
                line.append(over[team.id][competition.id])
            # preliminary results from runs
            elif competition.id in running[team.id] and competition.status == "OPEN":
                line.append(running[team.id][competition.id])
            else:
                line.append(None)
        table.append({"team":team,"results":line})
    return render(request,"contest/competitions.html",{"contest":contest,"teams":teams,"competitions":competitions,"table":table})


def contest_team(request,team_id):
    team = Team.objects.get(pk=team_id)
    competitions = []
    return render(request,"contest/teams.html",{"contest":team.contest,"team":team,"competitions":competitions})

def index(request):
    contests = list(Contest.objects.all())
    active_contests = filter(lambda x:x.status == ItemStates.OPEN ,contests)
    past_contests = filter(lambda x:x.status == ItemStates.CLOSED,contests)
    return render(request,"contest/index.html",{"active_contests":active_contests,"past_contests":past_contests})

## Automated run submission
## Request is POST json with items:
## teamtoken = access token from team Table, set by judge
## competitiontoken = access token from Competition table set by judge
## action = start or stop
## 
## Method will search team and competition according to the token.
## if action is start, it will create new run. It will do nothing if there is previous run with zero duration
## if action is stop, it will search previous run with zero duration and sets its duration with current time
def robot_action(request):
    # check request
    req = {}
    if request.type != "POST":
        raise BadRequest()
    try:
        # parse request
        req = json.loads(request.body)
    except:
        raise BadRequest()
    # validate request
    if "teamtoken" not in req:
        raise ValidationError()
    if "competitiontoken" not in req:
        raise ValidationError()
    if "action" not in req:
        raise ValidationError()
    if req["action"] not in set(["start","stop"]):
        raise ValidationError()
    # execute request
    team = Team.objects.get(token=req["teamtoken"])
    if team is None:
        raise PermissionDenied()
    competition = Competition.objects.get(token=req["competitiontoken"])
    if competition is None:
        raise PermissionDenied()
    runs = Run.objects.filter(team_id=team.id,competition_id=competition.id).order_by("-start_time").limit(1)
    is_running = False
    last_run = None
    response = "error"
    if len(runs) == 1:
        last_run = runs[0]
        if last_run.duration == 0:
            is_running = True
    if req["action"] == "start":
        if is_running:
            response = "already_running"
        elif last_run is not None:
            run = Run(start_time=datetime.now(),team=team,competition=competition)
            run.save()
            response = "started: " + run.start_time.isoformat()
    if req["action"] == "stop":
        if is_running:
            duration = (datetime.now() - last_run.start_time).total_seconds()
            last_run.duration = duration
            last_run.save()
            response = "end: " + str(duration)
        else:
            response = "not_running"
    return json.dumps({"result":response})



# Create your views here.
from . import views

