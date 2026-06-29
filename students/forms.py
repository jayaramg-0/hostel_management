from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    """Student Create/Update Form"""
    
    class Meta:
        model = Student
        fields = [
            'student_id', 'name', 'gender', 'date_of_birth', 
            'department', 'year', 'email', 'phone', 
            'parent_name', 'parent_contact', 'address', 
            'profile_photo', 'room', 'is_active'
        ]
        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Student ID'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Full Name'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Department'}),
            'year': forms.Select(attrs={'class': 'form-select'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'parent_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Parent Name'}),
            'parent_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Parent Contact'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter Address'}),
            'profile_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'room': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show available rooms
        from rooms.models import Room
        self.fields['room'].queryset = Room.objects.filter(status='available')
        self.fields['room'].required = False


class StudentSearchForm(forms.Form):
    """Student Search Form"""
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, ID, department...'
        })
    )
    department = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Department'
        })
    )
    year = forms.ChoiceField(
        required=False,
        choices=[('', 'All Years')] + list(Student.YEAR_CHOICES),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
