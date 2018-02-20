"""hand_tracker URL Configuration
"""

from django.urls import path

from app.views import *

urlpatterns = [
    path('', home, name='home'),
    path('student/', student_join, name='student'),
    path('student/class', class_run_student, name='student-class'),
    path('professor/', professor_create, name='professor'),
    path('professor/class', class_run_professor, name='professor-class'),
    path('professor/class/report', class_report, name='report'),
]
