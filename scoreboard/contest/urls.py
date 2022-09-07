from django.urls import path

from . import views

app_name = "contest"

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:competition_id>/board/', views.board, name='board'),
]
