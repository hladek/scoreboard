from django.urls import path

from . import views

app_name = "contest"

urlpatterns = [
    path('', views.index, name='index'),
    path('contest/<int:contest_id>', views.contest_competitions, name='contest_competitions'),
    path('team/<int:team_id>', views.contest_team, name='contest_team'),
    path('competition_board/<int:competition_id>', views.competition_board, name='competition_board'),
    path('frame/board/<int:competition_id>', views.frame_board, name='frame_board'),
]
