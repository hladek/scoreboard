from django.db import models
import datetime
from django.utils.translation import gettext_lazy as _

# Create your models here.
class ItemStates(models.TextChoices):
    OPEN = 'OPEN', _('Running')
    NEW = 'NEW', _('In preparation')
    CLOSED = 'CLOSED', _('In evaluation')
    OLD = 'OLD', _('Over')

class Contest(models.Model):
    # Contest contains more competitions
    name = models.CharField(max_length=200,help_text="Name of the contest. ")
    description = models.TextField(default="",help_text="Further description of the contest, such as time and place")
    status = models.CharField(
        max_length=6,
        choices=ItemStates.choices,
        default=ItemStates.NEW,
    )

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
    status = models.CharField(
        max_length=6,
        choices=ItemStates.choices,
        default=ItemStates.NEW,
    )
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE,help_text="Competition is one part of contest.")
    runs = models.ManyToManyField(Team,through="Run",related_name="runs",help_text="Competition has more runs from different teams.")
    participants = models.ManyToManyField(Team,help_text="There can be more participants in a competition")

    def __str__(self):
        return "Competition:{}@{}".format(self.name, self.contest.name)

class Run(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    score = models.IntegerField(help_text="Assigned by a Judge")
    judge_comment = models.CharField(max_length=200,help_text="Comment by a Judge",blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE,help_text="Who performed the run")
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE,help_text="source competition")
    @property
    def duration(self):
        dur = self.end_time - self.start_time
        return dur

    def __str__(self):
        return "Run:{}@{}".format(self.start_time, self.team.name)
