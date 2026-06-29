from django import forms
from .models import Attendance
from students.models import Student
from datetime import date


class AttendanceForm(forms.Form):
    """Form for marking attendance"""
    
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        initial=date.today
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically add fields for each active student
        students = Student.objects.filter(is_active=True, room__isnull=False)
        for student in students:
            self.fields[f'student_{student.pk}'] = forms.ChoiceField(
                choices=Attendance.STATUS_CHOICES,
                widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
                label=student.name,
                initial='present'
            )


class AttendanceFilterForm(forms.Form):
    """Form for filtering attendance records"""
    
    student = forms.ModelChoiceField(
        queryset=Student.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label='All Students'
    )
    from_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    to_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + list(Attendance.STATUS_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
