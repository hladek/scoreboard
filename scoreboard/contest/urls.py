from django.urls import path

from . import views

app_name = "contest"

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
]
