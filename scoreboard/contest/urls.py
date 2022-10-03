from django.urls import path

from . import views

app_name = "contest"

urlpatterns = [
    path('', views.index, name='index'),
    path('contest/<int:contest_id>', views.contest_competitions, name='contest_competitions'),
    path('board/<int:competition_id>', views.competition_board, name='competition_board'),
]
