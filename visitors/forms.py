from django import forms
from django.utils import timezone
from .models import Visitor


class VisitorForm(forms.ModelForm):
    """Visitor Registration Form"""
    
    class Meta:
        model = Visitor
        fields = ['visitor_name', 'student', 'relationship', 'phone', 'purpose', 'id_proof', 'remarks']
        widgets = {
            'visitor_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Visitor Name'
            }),
            'student': forms.Select(attrs={'class': 'form-select'}),
            'relationship': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Phone Number'
            }),
            'purpose': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Purpose of Visit'
            }),
            'id_proof': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ID Proof (Aadhar, PAN, etc.)'
            }),
            'remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Any remarks'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from students.models import Student
        self.fields['student'].queryset = Student.objects.filter(is_active=True)


class VisitorFilterForm(forms.Form):
    """Visitor Filter Form"""
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search visitor or student name...'
        })
    )
    date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    status = forms.ChoiceField(
        choices=[('', 'All'), ('in', 'Currently In'), ('out', 'Checked Out')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
