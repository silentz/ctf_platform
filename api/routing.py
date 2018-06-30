from django.urls import path
from . import consumers

urlpatterns = [
    path('ws/contest/<int:contest_id>/scoreboard/', consumers.ContestScoreboardConsumer),
    path('ws/contest/<int:contest_id>/notifications/', consumers.ContestNotificationConsumer),
    path('ws/scoreboard/', consumers.ScoreboardConsumer),
]