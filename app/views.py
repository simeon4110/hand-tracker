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
    """

    :param request:
    :return:
    """

    return render(
        request,
        'student.html',
        {
            'title': 'Home Page',
            'year': datetime.datetime.now().year,
        }
    )
