from django.db import models
import datetime

# Create your models here.

class Contest(models.Model):
    name = models.CharField(max_length=200,help_text="Name of the contest. COntest contains more competitions")
    description = models.TextField(default="",help_text="Further description of the contest, such as time and place")
    is_active = models.BooleanField(default=True,help_text="If the contest is running and can be used")
    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=200,help_text="Identifier of the team")
    description = models.TextField(default="",help_text="Team members and affiliation")
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE,help_text="a team belongs to a contest")
    def __str__(self):
        return "Team:{}@{}".format(self.name, self.contest.name)


class Competition(models.Model):
    name = models.CharField(max_length=200,help_text="Name of the competition.")
    description = models.TextField(default="Rules of the competition and description of the task,")
    is_active = models.BooleanField(default=True,help_text="Is competition runnig?")
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE,help_text="Competition is one part of contest.")
    runs = models.ManyToManyField(Team,through="Run",related_name="runs",help_text="Competition has more runs from different teams.")
    participants = models.ManyToManyField(Team,help_text="There can be more participants in a competition")

    def __str__(self):
        return "Competition:{}@{}".format(self.name, self.contest.name)

class Run(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    score = models.IntegerField(help_text="Assigned by a Judge")
    judge_comment = models.CharField(max_length=200,help_text="Comment by a Judge")
    team = models.ForeignKey(Team, on_delete=models.CASCADE,help_text="Who performed the run")
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE,help_text="source competition")
    @property
    def duration(self):
        dur = self.end_time - self.start_time
        return dur

    def __str__(self):
        return "Run:{}@{}".format(self.start_time, self.team.name)
