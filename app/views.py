"""
Definition of views.
"""
import datetime
import random

from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpRequest

from app.forms import ClassCreationForm
from app.forms import StudentJoinForm
from app.functions import send_email_report
from app.models import ClassRoom
from app.models import Student


def home(request):
    """
    The home page.
    :param request: The HTTP request.
    :return: A render of index.html.
    """
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'index.html',
        {
            'title': 'Home',
            'year': datetime.datetime.now().year
        }
    )


def professor_create(request):
    """
    The page where professors can create new classes.
    :param request: The HTTP request.
    :return: A render of professor.html.
    """
    assert isinstance(request, HttpRequest)

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


def student_join(request):
    """
    This is the page where students join a running class.
    :param request: The HTTP request.
    :return: A render of student.html.
    """
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'student.html',
        {
            'title': 'Join Class',
            'year': datetime.datetime.now().year,
            'form': StudentJoinForm,
        }
    )


def class_run_student(request):
    """
    The student page (i.e. the hand's up / hand's down page.)
    :param request: The HTTP request.
    :return: A render of classroom-student.html
    """
    assert isinstance(request, HttpRequest)

    if request.method == 'POST':
        form = StudentJoinForm(request.POST)

        if form.is_valid():
            class_number = form.cleaned_data.get("class_number")
            student_name = form.cleaned_data.get("student_name")

            # This is good enough. No need for more.
            try:
                ClassRoom.objects.get(class_number=class_number)
            except Exception as e:
                messages.warning(request, "An error occurred: " + str(e))
                return redirect("student")

            # Check if the student already exists, if not create the student,
            # if the student exists AND is already in the correct class, use
            # the existing student object. If the student exists but is in the
            # wrong class, reset the student's counters and move into class.
            if not Student.objects.filter(student_name=student_name).exists():
                new_student = Student(
                    student_name=student_name,
                    acknowledged=0,
                    modifier=0,
                    class_room=ClassRoom.objects.get(class_number=class_number)
                )

                new_student.save()
                student_id = new_student.id
            else:
                student = Student.objects.get(student_name=student_name)
                if student.class_room.class_number != class_number:
                    student.class_room = ClassRoom.objects.get(
                        class_number=class_number)
                    student.acknowledged = 0
                    student.modifier = 0
                    student.save()
                    student_id = student.id

            return render(
                request,
                'classroom-student.html',
                {
                    'title': 'Hand Tracker',
                    'student_name': student_name,
                    'student_id': student_id,
                    'class_number': class_number,
                }
            )


def class_run_professor(request):
    """
    This is the page where the professors create new classes.
    :param request: The HTTP request.
    :return: A render of classroom-professor.html
    """
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        form = ClassCreationForm(request.POST)

        if form.is_valid():
            class_number = form.cleaned_data.get("class_number")

            # This check is needed to prevent duplicate classes from being
            # formed.
            if not ClassRoom.objects.filter(class_number=class_number).exists():
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

    # If the form is not valid or the request method is not post, add an error
    # and redirect.
    messages.warning(request, "Something went wrong, please try again.")
    return redirect("professor")


def class_report(request):
    """
    Ends a class and displays a beautiful report.
    :param request: The HTTP request.
    :return: A render of classroom-report.html.
    """
    assert isinstance(request, HttpRequest)

    # Check to ensure the request contains a class_id.
    if request.GET.get("class_id") is not None:
        class_number = request.GET.get("class_id")

        try:
            class_room = ClassRoom.objects.get(class_number=class_number)
        except Exception as e:
            messages.warning(request, "An error occurred: " + str(e))
            return redirect("professor")

        report_list = []

        student_list = Student.objects.filter(class_room=class_room).values_list(
            "student_name", "acknowledged")

        # Append all the student data to the student list, delete the student.
        for student in student_list:
            report_list.append([student[0], student[1]])

        # Attempt to send the email report, post error if fails.
        try:
            send_email_report(class_room.professor_email, report_list,
                              str(class_room.class_number))
            messages.success(request, "Email report sent!")
        except Exception as e:
            messages.warning(request, "An error occurred while sending"
                                      " the email report: %s" % e)

        # Delete the classroom.
        class_number = class_room.class_number
        class_room.delete()

        return render(
            request,
            'classroom-report.html',
            {
                'title': 'End of Class Report',
                'year': datetime.datetime.now().year,
                'report_data': report_list,
                'class_number': class_number,
            }
        )
