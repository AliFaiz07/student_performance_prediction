# performance/forms.py

from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'name',
            'email',
            'mobile',
            'attendance',
            'assignment_score',
            'test_score',
            'teacher_feedback'
        ]

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'mobile', 'pin']
