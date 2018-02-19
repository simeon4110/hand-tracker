"""
Definition of views.
"""

import datetime
from datetime import timezone

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect

from app.forms import *


def home(request):
    return render(
        request,
        'index.html',
        {
            'title': 'Home',
            'year': datetime.datetime.now().year
        }
    )


def professor_create(request):
    return render(
        request,
        'professor.html',
        {
            'title': 'Create Class',
            'year': datetime.datetime.now().year,
            'form': ClassCreationForm,
        }
    )


def class_run_student(request):
    return render(
        request,
        'classroom-student.html',
        {
            'title': 'Hand Tracker'
        }
    )


def class_run_professor(request):
    return None


def student_join(request):
    """

    :param request:
    :return:
    """

    return render(
        request,
        'student.html',
        {
            'title': 'Join Class',
            'year': datetime.datetime.now().year,
            'form': StudentJoinForm,
        }
    )
