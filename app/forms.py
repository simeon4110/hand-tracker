import random

from django import forms
from django.utils.translation import ugettext_lazy as _

from app.models import *


class StudentJoinForm(forms.ModelForm):
    class_number = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'i.e. 000000',
    }))

    class Meta:
        model = Student
        fields = ['student_name']
        labels = ({'student_name': _('Your name.')})
        widgets = {
            'student_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'i.e. Becky Smith'
            })
        }


class ClassCreationForm(forms.ModelForm):
    class Meta:
        model = ClassRoom
        ClassRoom.class_number = random.randint(1, 999999)

        fields = ['professor_name', 'professor_email']
        labels = ({'professor_name': _('Your name.'),
                   'professor_email': _('Your email.')})
        widgets = {
            'professor_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name',
            }),
            'professor_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name',
            })
        }
