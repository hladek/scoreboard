from django.db import models
import datetime
from django.utils.translation import gettext_lazy as _
#from ckeditor.fields import RichTextField

# Create your models here.
class ItemStates(models.TextChoices):
    NEW = 'NEW', _('In preparation')
    OPEN = 'OPEN', _('Open')
    CLOSED = 'CLOSED', _('Closed')
    DELETED = 'DELETED', _('Deleted')

class Contest(models.Model):
    # Contest contains more competitions
    name = models.CharField(max_length=200,help_text="Name of the contest. ")
    description = models.TextField(default="",blank=True,help_text="Short description of the contest, such as time and place")
    status = models.CharField(
        max_length=24,
        choices=ItemStates.choices,
        default=ItemStates.NEW,
    )

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=200,help_text="Identifier of the team")
    description = models.TextField(default="",blank=True,help_text="Team members and affiliation")
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE,help_text="a team belongs to a contest")

    token = models.CharField(max_length=200,default="",blank=True,help_text="Token for run submissions")
    def __str__(self):
        return "Team:{}@{}".format(self.name, self.contest.name)


class Competition(models.Model):
    name = models.CharField(max_length=200,help_text="Name of the competition.")
    description = models.TextField(default="",blank=True,help_text="Rules of the competition and description of the task,")
    status = models.CharField(
        max_length=24,
        choices=ItemStates.choices,
        default=ItemStates.NEW,
    )
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE,help_text="Competition is one part of contest.")
    runs = models.ManyToManyField(Team,through="Run",related_name="runs",help_text="Competition has more runs from different teams.")

    def __str__(self):
        return "Competition:{}@{}".format(self.name, self.contest.name)

class Result(models.Model):
    score = models.IntegerField()
    comment = models.TextField(default="",blank=True,help_text="Comment to the participation")
    # TODO - add constraint to Team to current contest
    team = models.ForeignKey(Team, on_delete=models.CASCADE,help_text="Competition is one part of contest.")
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE,help_text="Competition is one part of contest.")
    class Meta:
        unique_together = (("team","competition"),)
    def __str__(self):
        return "Result:{}@{}".format(self.team.name, self.competition.name)

class Run(models.Model):
    start_time = models.DateTimeField()
    # in seconds
    duration = models.IntegerField(blank=True)
    score = models.IntegerField(help_text="Assigned by a Judge",blank=True,null=True)
    judge_comment = models.CharField(max_length=200,help_text="Comment by a Judge",blank=True)
    # TODO - add constraint to Team to current competition contest
    team = models.ForeignKey(Team, on_delete=models.CASCADE,help_text="Who performed the run")
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE,help_text="source competition")

    def __str__(self):
        return "Run:{}@{}".format(self.start_time, self.team.name)
