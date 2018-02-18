"""hand_tracker URL Configuration
"""

from django.urls import path

from app.views import *

urlpatterns = [
    path('', home, name='home'),
    path('student/', student_join, name='student'),
    path('professor/', professor_create, name='professor'),
    path('class/', class_run, name='class'),
]
