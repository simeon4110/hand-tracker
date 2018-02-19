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
            'class_number': random.randint(100000, 999999),
            'form': ClassCreationForm,
        }
    )


def class_run_student(request):
    if request.method == 'POST':
        form = StudentJoinForm(request.POST)
        if form.is_valid():
            class_number = form.cleaned_data.get("class_number")
            student_name = form.cleaned_data.get("student_name")

            new_student = Student(
                student_name=student_name,
                acknowledged=0,
                modifier=0,
                class_room=ClassRoom.objects.get(class_number=class_number)
            )

            new_student.save()

            return render(
                request,
                'classroom-student.html',
                {
                    'title': 'Hand Tracker',
                    'student_name': student_name,
                    'class_number': class_number,
                }
            )


def class_run_professor(request):
    if request.method == "POST":
        form = ClassCreationForm(request.POST)
        if form.is_valid():
            class_number = form.cleaned_data.get("class_number")
            professor_name = form.cleaned_data.get("professor_name")
            professor_email = form.cleaned_data.get("professor_email")
            form.save()

            return render(
                request,
                'classroom-professor.html',
                {
                    'title': 'Hand Tracker',
                    'year': datetime.datetime.now().year,
                    'class_number': class_number,
                }
            )

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
