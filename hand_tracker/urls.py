"""hand_tracker URL Configuration
"""

from django.urls import path

from app.views import *

urlpatterns = [
    path('', home),
    path('student/', student_join),
    path('professor/', professor_create),
    path('class/', class_run),
]
