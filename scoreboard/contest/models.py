from django.db import models

# Create your models here.

class Contest(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default="")
    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default="")
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    def __str__(self):
        return "Team:{}@{}".format(self.name, self.contest.name)


class Competition(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default="")
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    runs = models.ManyToManyField(Team,through="Run",related_name="runs")
    participants = models.ManyToManyField(Team)

    def __str__(self):
        return "Competition:{}@{}".format(self.name, self.contest.name)

class Run(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    score = models.IntegerField()
    judge_comment = models.CharField(max_length=200)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    def __str__(self):
        return "Run:{}@{}".format(self.start_time, self.team.name)
