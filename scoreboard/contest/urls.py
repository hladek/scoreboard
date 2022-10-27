from django.urls import path

from . import views

app_name = "contest"

urlpatterns = [
    path('', views.index, name='index'),
    path('contest/<int:contest_id>', views.contest_competitions, name='contest_competitions'),
    path('team/<int:team_id>', views.contest_team, name='contest_team'),
    path('board/<int:competition_id>', views.competition_board, name='competition_board'),
]
