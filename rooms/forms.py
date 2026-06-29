from django import forms
from .models import Room


class RoomForm(forms.ModelForm):
    """Room Create/Update Form"""
    
    class Meta:
        model = Room
        fields = ['room_number', 'floor', 'capacity', 'description']
        widgets = {
            'room_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Room Number (e.g., 101, A-201)'
            }),
            'floor': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Floor Number',
                'min': 0
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Room Capacity',
                'min': 1
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter Room Description (optional)'
            }),
        }


class RoomAllocationForm(forms.Form):
    """Form for allocating room to student"""
    
    student = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from students.models import Student
        # Only show students without rooms
        self.fields['student'].queryset = Student.objects.filter(room__isnull=True, is_active=True)
